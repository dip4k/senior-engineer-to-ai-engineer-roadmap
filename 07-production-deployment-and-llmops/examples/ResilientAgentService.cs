// ============================================================================
// File: ResilientAgentService.cs
// Framework: .NET 9 / ASP.NET Core 9
// Dependencies: Polly.Core (v8.x), Microsoft.Extensions.AI, StackExchange.Redis
// ============================================================================

using System.Runtime.CompilerServices;
using System.Security.Cryptography;
using System.Text;
using System.Text.Json;
using Microsoft.AspNetCore.Mvc;
using Polly;
using Polly.CircuitBreaker;
using Polly.Retry;
using StackExchange.Redis;

namespace Enterprise.Ai.Gateway;

// -----------------------------------------------------------------------------
// Request & Domain Models
// -----------------------------------------------------------------------------
public sealed record AgentChatRequest(
    string Prompt,
    string TenantId,
    string UserId,
    int MaxTokens = 1024,
    double Temperature = 0.7);

public sealed record StreamTokenPayload(string Token, bool IsCached, long ElapsedMs);

// -----------------------------------------------------------------------------
// Port Interface: AI Provider Client
// -----------------------------------------------------------------------------
public interface IModelProviderClient
{
    IAsyncEnumerable<string> GenerateStreamAsync(
        string prompt, 
        int maxTokens, 
        double temperature, 
        CancellationToken cancellationToken);
}

// -----------------------------------------------------------------------------
// Primary Provider Implementation (Azure OpenAI / Anthropic Adapter)
// -----------------------------------------------------------------------------
public sealed class PrimaryModelProviderClient : IModelProviderClient
{
    private readonly HttpClient _httpClient;
    private readonly ILogger<PrimaryModelProviderClient> _logger;

    public PrimaryModelProviderClient(HttpClient httpClient, ILogger<PrimaryModelProviderClient> logger)
    {
        _httpClient = httpClient;
        _logger = logger;
    }

    public async IAsyncEnumerable<string> GenerateStreamAsync(
        string prompt, 
        int maxTokens, 
        double temperature, 
        [EnumeratorCancellation] CancellationToken cancellationToken)
    {
        _logger.LogInformation("Calling Primary LLM Provider (Claude 3.7 / GPT-4.5 / o3)...");
        
        // Simulating streaming chunks from underlying provider SDK
        string[] simulatedTokens = ["Enterprise ", "resilience ", "achieved ", "via ", ".NET 9 ", "and ", "Polly v8."];
        
        foreach (var token in simulatedTokens)
        {
            cancellationToken.ThrowIfCancellationRequested();
            await Task.Delay(40, cancellationToken); // Simulating 40ms token throughput (~25 tok/s)
            yield return token;
        }
    }
}

// -----------------------------------------------------------------------------
// Secondary Fallback Provider Implementation (Google Cloud Vertex AI)
// -----------------------------------------------------------------------------
public sealed class SecondaryModelProviderClient : IModelProviderClient
{
    private readonly ILogger<SecondaryModelProviderClient> _logger;

    public SecondaryModelProviderClient(ILogger<SecondaryModelProviderClient> logger)
    {
        _logger = logger;
    }

    public async IAsyncEnumerable<string> GenerateStreamAsync(
        string prompt, 
        int maxTokens, 
        double temperature, 
        [EnumeratorCancellation] CancellationToken cancellationToken)
    {
        _logger.LogWarning("PRIMARY DEGRADED: Executing Secondary Fallback Provider (Vertex Gemini 1.5)...");
        
        string[] simulatedTokens = ["Fallback ", "response ", "from ", "Secondary ", "Cloud ", "Provider."];
        
        foreach (var token in simulatedTokens)
        {
            cancellationToken.ThrowIfCancellationRequested();
            await Task.Delay(30, cancellationToken);
            yield return token;
        }
    }
}

// -----------------------------------------------------------------------------
// Resilient Gateway Orchestrator with Polly v8 & Redis Cache
// -----------------------------------------------------------------------------
public sealed class AgentOrchestrator
{
    private readonly IModelProviderClient _primaryClient;
    private readonly IModelProviderClient _secondaryClient;
    private readonly IConnectionMultiplexer _redis;
    private readonly ResiliencePipeline _resiliencePipeline;
    private readonly ILogger<AgentOrchestrator> _logger;

    public AgentOrchestrator(
        IModelProviderClient primaryClient,
        IModelProviderClient secondaryClient,
        IConnectionMultiplexer redis,
        ILogger<AgentOrchestrator> logger)
    {
        _primaryClient = primaryClient;
        _secondaryClient = secondaryClient;
        _redis = redis;
        _logger = logger;

        // Build Polly v8 Composite Resilience Pipeline:
        // Retry (with exponential backoff and jitter) + Circuit Breaker
        _resiliencePipeline = new ResiliencePipelineBuilder()
            .AddRetry(new RetryStrategyOptions
            {
                MaxRetryAttempts = 3,
                Delay = TimeSpan.FromMilliseconds(500),
                BackoffType = DelayBackoffType.Exponential,
                UseJitter = true,
                ShouldHandle = new PredicateBuilder().Handle<HttpRequestException>().Handle<TimeoutException>()
            })
            .AddCircuitBreaker(new CircuitBreakerStrategyOptions
            {
                FailureRatio = 0.5,
                SamplingDuration = TimeSpan.FromSeconds(30),
                MinimumThroughput = 10,
                BreakDuration = TimeSpan.FromSeconds(15),
                OnOpened = args =>
                {
                    _logger.LogError("CRITICAL: Primary LLM Circuit Breaker tripped OPEN! Diverting to Secondary.");
                    return ValueTask.CompletedTask;
                },
                OnClosed = args =>
                {
                    _logger.LogInformation("Primary LLM Circuit Breaker RESET to CLOSED.");
                    return ValueTask.CompletedTask;
                }
            })
            .Build();
    }

    public async IAsyncEnumerable<StreamTokenPayload> ExecuteStreamAsync(
        AgentChatRequest request, 
        [EnumeratorCancellation] CancellationToken cancellationToken)
    {
        var db = _redis.GetDatabase();
        var cacheKey = ComputeSha256CacheKey(request.TenantId, request.Prompt);
        
        // 1. Check L1 Exact Redis Cache
        string? cachedValue = await db.StringGetAsync(cacheKey);
        if (!string.IsNullOrEmpty(cachedValue))
        {
            _logger.LogInformation("Cache HIT for Tenant {TenantId}", request.TenantId);
            yield return new StreamTokenPayload(cachedValue, IsCached: true, ElapsedMs: 5);
            yield break;
        }

        // 2. Cache Miss: Execute Resilient Stream with Fallback
        var responseBuffer = new StringBuilder();
        var stopwatch = System.Diagnostics.Stopwatch.StartNew();

        IAsyncEnumerable<string>? stream = null;

        try
        {
            // Execute within Circuit Breaker & Retry Pipeline
            stream = _resiliencePipeline.Execute(
                state => _primaryClient.GenerateStreamAsync(state.Prompt, state.MaxTokens, state.Temperature, cancellationToken),
                request);
        }
        catch (BrokenCircuitException)
        {
            _logger.LogWarning("Circuit open. Diverting immediately to secondary provider.");
            stream = _secondaryClient.GenerateStreamAsync(request.Prompt, request.MaxTokens, request.Temperature, cancellationToken);
        }
        catch (Exception ex)
        {
            _logger.LogError(ex, "Primary provider failed after retries. Invoking secondary.");
            stream = _secondaryClient.GenerateStreamAsync(request.Prompt, request.MaxTokens, request.Temperature, cancellationToken);
        }

        await foreach (var token in stream.WithCancellation(cancellationToken))
        {
            responseBuffer.Append(token);
            yield return new StreamTokenPayload(token, IsCached: false, ElapsedMs: stopwatch.ElapsedMilliseconds);
        }

        // Asynchronously persist completed response to Redis (TTL 24 hours)
        var fullText = responseBuffer.ToString();
        if (!string.IsNullOrEmpty(fullText) && !cancellationToken.IsCancellationRequested)
        {
            _ = Task.Run(() => db.StringSetAsync(cacheKey, fullText, TimeSpan.FromHours(24)), CancellationToken.None);
        }
    }

    private static string ComputeSha256CacheKey(string tenantId, string prompt)
    {
        var raw = $"{tenantId}:{prompt.Trim().ToLowerInvariant()}";
        var bytes = SHA256.HashData(Encoding.UTF8.GetBytes(raw));
        return $"cache:tenant:{tenantId}:{Convert.ToHexString(bytes)}";
    }
}

// -----------------------------------------------------------------------------
// ASP.NET Core 9 Minimal API Controller
// -----------------------------------------------------------------------------
[ApiController]
[Route("api/v1/agent")]
public sealed class AgentController : ControllerBase
{
    private readonly AgentOrchestrator _orchestrator;

    public AgentController(AgentOrchestrator orchestrator)
    {
        _orchestrator = orchestrator;
    }

    [HttpPost("stream")]
    public async Task StreamPrompt(
        [FromBody] AgentChatRequest request, 
        CancellationToken cancellationToken)
    {
        Response.ContentType = "text/event-stream";
        Response.Headers.Append("Cache-Control", "no-cache");
        Response.Headers.Append("X-Accel-Buffering", "no");

        try
        {
            await foreach (var payload in _orchestrator.ExecuteStreamAsync(request, cancellationToken))
            {
                var sseMessage = $"data: {JsonSerializer.Serialize(payload)}\n\n";
                await Response.WriteAsync(sseMessage, cancellationToken);
                await Response.Body.FlushAsync(cancellationToken);
            }

            await Response.WriteAsync("data: [DONE]\n\n", cancellationToken);
            await Response.Body.FlushAsync(cancellationToken);
        }
        catch (OperationCanceledException)
        {
            // Client closed browser or disconnected; gracefully end HTTP request
        }
    }
}
