"""
Token-Bucket Rate Limiter for AgentForge Gateway.
Protects against upstream provider 429 errors and enforces per-tenant TPM/RPM quotas.
"""

import time
from typing import Dict, Tuple

class TokenBucketLimiter:
    """
    Implements a leaky token-bucket algorithm for Requests-Per-Minute (RPM)
    and Tokens-Per-Minute (TPM).
    """
    def __init__(self, default_rpm: int = 60, default_tpm: int = 100_000):
        self.default_rpm = default_rpm
        self.default_tpm = default_tpm
        # tenant_id -> (current_tokens, last_refill_timestamp)
        self._req_buckets: Dict[str, Tuple[float, float]] = {}
        self._tok_buckets: Dict[str, Tuple[float, float]] = {}

    def _refill(self, current: float, last_time: float, capacity: float, rate_per_sec: float) -> Tuple[float, float]:
        now = time.time()
        elapsed = now - last_time
        new_tokens = min(capacity, current + elapsed * rate_per_sec)
        return new_tokens, now

    def check_and_consume(self, tenant_id: str, estimated_tokens: int = 500) -> Tuple[bool, str]:
        now = time.time()
        rpm_cap = float(self.default_rpm)
        tpm_cap = float(self.default_tpm)
        rpm_rate = rpm_cap / 60.0
        tpm_rate = tpm_cap / 60.0

        req_tokens, req_time = self._req_buckets.get(tenant_id, (rpm_cap, now))
        req_tokens, req_time = self._refill(req_tokens, req_time, rpm_cap, rpm_rate)

        tok_tokens, tok_time = self._tok_buckets.get(tenant_id, (tpm_cap, now))
        tok_tokens, tok_time = self._refill(tok_tokens, tok_time, tpm_cap, tpm_rate)

        if req_tokens < 1.0:
            return False, f"RPM limit exceeded for tenant {tenant_id}. Try again in {1.0 / rpm_rate:.1f}s."
        
        if tok_tokens < estimated_tokens:
            return False, f"TPM limit exceeded for tenant {tenant_id}. Required {estimated_tokens}, available {tok_tokens:.0f}."

        # Consume
        self._req_buckets[tenant_id] = (req_tokens - 1.0, req_time)
        self._tok_buckets[tenant_id] = (tok_tokens - float(estimated_tokens), tok_time)
        return True, "OK"
