"""
Token-Bucket Rate Limiter for AgentForge Gateway.
Protects against upstream provider 429 errors and enforces per-tenant TPM/RPM quotas.
Supports streaming upfront token reservation and post-generation settlement.
"""

import time
from typing import Dict, Tuple

class TokenBucketLimiter:
    """
    Implements a token-bucket algorithm for Requests-Per-Minute (RPM)
    and Tokens-Per-Minute (TPM) with upfront reservation and post-stream settlement.
    """
    def __init__(self, default_rpm: int = 60, default_tpm: int = 100_000):
        self.default_rpm = float(default_rpm)
        self.default_tpm = float(default_tpm)
        self.rpm_rate = self.default_rpm / 60.0
        self.tpm_rate = self.default_tpm / 60.0
        
        # tenant_id -> (current_tokens, last_refill_timestamp)
        self._req_buckets: Dict[str, Tuple[float, float]] = {}
        self._tok_buckets: Dict[str, Tuple[float, float]] = {}

    def _refill(self, current: float, last_time: float, capacity: float, rate_per_sec: float) -> Tuple[float, float]:
        now = time.time()
        elapsed = now - last_time
        new_tokens = min(capacity, current + elapsed * rate_per_sec)
        return new_tokens, now

    def acquire(self, tenant_id: str, estimated_tokens: int = 500) -> Tuple[bool, str]:
        """
        Reserves request capacity and estimated tokens upfront before initiating inference.
        """
        now = time.time()
        req_tokens, req_time = self._req_buckets.get(tenant_id, (self.default_rpm, now))
        req_tokens, req_time = self._refill(req_tokens, req_time, self.default_rpm, self.rpm_rate)

        tok_tokens, tok_time = self._tok_buckets.get(tenant_id, (self.default_tpm, now))
        tok_tokens, tok_time = self._refill(tok_tokens, tok_time, self.default_tpm, self.tpm_rate)

        if req_tokens < 1.0:
            return False, f"RPM limit exceeded for tenant {tenant_id}. Try again in {1.0 / self.rpm_rate:.1f}s."
        
        if tok_tokens < estimated_tokens:
            return False, f"TPM limit exceeded for tenant {tenant_id}. Required {estimated_tokens}, available {tok_tokens:.0f}."

        # Deduct reservation
        self._req_buckets[tenant_id] = (req_tokens - 1.0, req_time)
        self._tok_buckets[tenant_id] = (tok_tokens - float(estimated_tokens), tok_time)
        return True, "OK"

    def settle(self, tenant_id: str, estimated_tokens: int, actual_tokens: int) -> None:
        """
        Reconciles the difference between reserved tokens and actual tokens used
        once a streaming response finishes.
        """
        now = time.time()
        delta = float(estimated_tokens - actual_tokens)
        if tenant_id in self._tok_buckets:
            tok_tokens, tok_time = self._tok_buckets[tenant_id]
            tok_tokens, tok_time = self._refill(tok_tokens, tok_time, self.default_tpm, self.tpm_rate)
            # Add back unspent tokens or charge overage, capped at maximum capacity
            adjusted = min(self.default_tpm, tok_tokens + delta)
            self._tok_buckets[tenant_id] = (adjusted, tok_time)

    def check_and_consume(self, tenant_id: str, estimated_tokens: int = 500) -> Tuple[bool, str]:
        """Backward-compatible synchronous helper."""
        return self.acquire(tenant_id, estimated_tokens)
