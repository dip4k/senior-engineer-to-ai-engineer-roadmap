"""
Production Enterprise AI Gateway Microservice
Stack: FastAPI, LiteLLM Router, Redis Semantic Cache, SSE Streaming
"""

import os
import json
import time
import hashlib
import logging
import asyncio
from typing import AsyncGenerator, Optional
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException, Request, Depends, status
from fastapi.responses import StreamingResponse
from pydantic import BaseModel, Field
import redis.asyncio as aioredis
from litellm import Router

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(name)s: %(message)s")
logger = logging.getLogger("EnterpriseAIGateway")

# -----------------------------------------------------------------------------
# Configuration & Lifespan
# -----------------------------------------------------------------------------
REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")
SEMANTIC_SIMILARITY_THRESHOLD = 0.92
CACHE_TTL_SECONDS = 86400  # 24 Hours

# Global Singletons
redis_client: Optional[aioredis.Redis] = None
llm_router: Optional[Router] = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    global redis_client, llm_router
    logger.info("Initializing Enterprise AI Gateway infrastructure...")
    
    # 1. Initialize Redis Connection Pool
    redis_client = aioredis.from_url(
        REDIS_URL, 
        encoding="utf-8", 
        decode_responses=True,
        max_connections=50
    )
    await redis_client.ping()
    logger.info("Connected to Redis Cache.")

    # 2. Initialize LiteLLM Router with Multi-Provider Fallbacks & Retries
    model_list = [
        {
            "model_name": "enterprise-chat",
            "litellm_params": {
                "model": "anthropic/claude-3-7-sonnet-latest",
                "api_key": os.getenv("ANTHROPIC_API_KEY", "mock-key"),
                "rpm": 1000,
                "tpm": 80000,
            },
        },
        {
            "model_name": "enterprise-chat",
            "litellm_params": {
                "model": "azure/gpt-4.5",
                "api_key": os.getenv("AZURE_OPENAI_API_KEY", "mock-key"),
                "api_base": os.getenv("AZURE_OPENAI_ENDPOINT", "https://mock.openai.azure.com/"),
                "api_version": "2024-08-01-preview",
                "rpm": 1500,
                "tpm": 120000,
            },
        },
        {
            "model_name": "enterprise-chat-fallback",
            "litellm_params": {
                "model": "gemini/gemini-2.5-flash",
                "api_key": os.getenv("GEMINI_API_KEY", "mock-key"),
                "rpm": 3000,
                "tpm": 200000,
            },
        },
    ]

    llm_router = Router(
        model_list=model_list,
        fallbacks=[{"enterprise-chat": ["enterprise-chat-fallback"]}],
        num_retries=3,
        timeout=30.0,
        retry_after=2,
        routing_strategy="latency-based-routing"
    )
    logger.info("LiteLLM Router initialized with 3 tiered provider models.")
    
    yield
    
    logger.info("Shutting down AI Gateway...")
    if redis_client:
        await redis_client.close()

app = FastAPI(title="Enterprise AI Gateway", version="1.0.0", lifespan=lifespan)

# -----------------------------------------------------------------------------
# Domain Schemas
# -----------------------------------------------------------------------------
class ChatRequest(BaseModel):
    prompt: str = Field(..., min_length=1, max_length=10000, description="User instruction or prompt")
    tenant_id: str = Field(..., min_length=1, max_length=64, description="Tenant identifier for multi-tenant isolation")
    user_id: str = Field(..., min_length=1, max_length=64, description="Unique user identifier")
    max_tokens: int = Field(default=1024, ge=1, le=4096)
    temperature: float = Field(default=0.7, ge=0.0, le=2.0)

# -----------------------------------------------------------------------------
# Cache Subsystem (Deterministic L1 Hash + Metadata)
# -----------------------------------------------------------------------------
def compute_cache_key(tenant_id: str, prompt: str) -> str:
    normalized = prompt.strip().lower()
    digest = hashlib.sha256(f"{tenant_id}:{normalized}".encode("utf-8")).hexdigest()
    return f"llm_cache:{tenant_id}:{digest}"

async def get_exact_cache(tenant_id: str, prompt: str) -> Optional[str]:
    if not redis_client:
        return None
    key = compute_cache_key(tenant_id, prompt)
    return await redis_client.get(key)

async def set_exact_cache(tenant_id: str, prompt: str, content: str):
    if not redis_client:
        return
    key = compute_cache_key(tenant_id, prompt)
    await redis_client.set(key, content, ex=CACHE_TTL_SECONDS)

# -----------------------------------------------------------------------------
# Streaming Token Generator with Cancellation Propagation
# -----------------------------------------------------------------------------
async def token_streamer(
    request: Request,
    chat_req: ChatRequest,
    router: Router
) -> AsyncGenerator[str, None]:
    """
    Streams tokens over SSE while monitoring client connection liveness.
    Halts upstream LLM generation immediately if the client disconnects.
    """
    start_time = time.perf_counter()
    full_response_accumulator = []
    
    # Check L1 Exact Cache
    cached_content = await get_exact_cache(chat_req.tenant_id, chat_req.prompt)
    if cached_content:
        logger.info(f"L1 Exact Cache Hit for Tenant {chat_req.tenant_id}")
        chunk_payload = {
            "choices": [{"delta": {"content": cached_content}}],
            "cached": True,
            "latency_ms": round((time.perf_counter() - start_time) * 1000, 2)
        }
        yield f"data: {json.dumps(chunk_payload)}\n\n"
        yield "data: [DONE]\n\n"
        return

    # Cache Miss: Call Router Stream
    try:
        messages = [{"role": "user", "content": chat_req.prompt}]
        response = await router.acompletion(
            model="enterprise-chat",
            messages=messages,
            max_tokens=chat_req.max_tokens,
            temperature=chat_req.temperature,
            stream=True
        )

        first_token = True
        async for chunk in response:
            # CRITICAL: Detect client disconnection to kill zombie generation
            if await request.is_disconnected():
                logger.warning(f"Client disconnected during streaming for Tenant {chat_req.tenant_id}. Halting generation.")
                break

            delta_content = chunk.choices[0].delta.content or ""
            if delta_content:
                full_response_accumulator.append(delta_content)
                payload = {
                    "choices": [{"delta": {"content": delta_content}}],
                    "cached": False
                }
                if first_token:
                    ttft = round((time.perf_counter() - start_time) * 1000, 2)
                    payload["ttft_ms"] = ttft
                    first_token = False
                    logger.info(f"TTFT for Tenant {chat_req.tenant_id}: {ttft}ms")

                yield f"data: {json.dumps(payload)}\n\n"

        yield "data: [DONE]\n\n"

        # Asynchronously store completed generation in cache
        complete_text = "".join(full_response_accumulator)
        if complete_text:
            asyncio.create_task(set_exact_cache(chat_req.tenant_id, chat_req.prompt, complete_text))

    except Exception as ex:
        logger.error(f"Routing/Generation Exception: {str(ex)}", exc_info=True)
        err_payload = {"error": "Upstream AI provider error. Resiliency policy engaged.", "details": str(ex)}
        yield f"data: {json.dumps(err_payload)}\n\n"
        yield "data: [DONE]\n\n"

# -----------------------------------------------------------------------------
# API Route Definitions
# -----------------------------------------------------------------------------
@app.post("/v1/chat/completions/stream", response_class=StreamingResponse)
async def stream_chat_completion(
    chat_req: ChatRequest,
    request: Request
):
    if not llm_router:
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail="AI Gateway not initialized.")

    return StreamingResponse(
        token_streamer(request, chat_req, llm_router),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache, no-transform",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no"  # Instructs NGINX/reverse proxies not to buffer
        }
    )

@app.get("/healthz")
async def health_check():
    return {"status": "healthy", "service": "enterprise-ai-gateway"}
