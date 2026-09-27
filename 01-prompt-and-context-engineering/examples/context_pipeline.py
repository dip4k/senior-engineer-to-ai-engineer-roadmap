"""
production_context_pipeline.py
Production-grade prompt compiler with Anthropic Prompt Caching and Pydantic v2 validation.
"""
import os
import re
from typing import List, Literal, Optional
from pydantic import BaseModel, Field, ValidationError
import anthropic

# 1. Define Strict Pydantic Schema
class ComplianceEvaluation(BaseModel):
    policy_id: str = Field(description="Corporate policy identifier")
    compliance_status: Literal["COMPLIANT", "VIOLATION", "NEEDS_MANUAL_REVIEW"]
    severity: Literal["CRITICAL", "HIGH", "MEDIUM", "LOW", "NONE"]
    violated_clauses: List[str] = Field(default_factory=list)
    remediation_summary: Optional[str] = Field(None, max_length=500)

class EnterprisePromptCompiler:
    def __init__(self):
        self.client = anthropic.Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))
        
        # 2. Large Static Policy Manual (Immutable -> Prime Cache Target)
        self.STATIC_POLICY_MANUAL = """
        <enterprise_policy_manual>
        SECTION 1: DATA PROTECTION & ENCRYPTION
        1.1 All customer PII must be encrypted at rest using AES-256 and in transit via TLS 1.3.
        1.2 No raw credentials, API keys, or JWT tokens may be logged in plaintext application telemetry.
        
        SECTION 2: TRANSACTION LIMITS & APPROVALS
        2.1 Financial transfers exceeding $50,000 USD require dual-signature multi-factor authorization.
        2.2 International wires to high-risk jurisdictions require compliance officer sign-off.
        </enterprise_policy_manual>
        """

    def sanitize_input(self, text: str) -> str:
        """Prevent XML delimiter smuggling."""
        return text.replace("<", "&lt;").replace(">", "&gt;")

    def evaluate_audit_event(self, audit_log: str) -> ComplianceEvaluation:
        sanitized_log = self.sanitize_input(audit_log)

        # 3. Construct Context Hierarchy with Explicit Cache Breakpoint
        response = self.client.messages.create(
            model="claude-3-7-sonnet-latest",
            max_tokens=1024,
            temperature=0.0,
            system=[
                {
                    "type": "text",
                    "text": (
                        "You are an automated enterprise compliance auditor. Evaluate the audit event "
                        "against the enterprise policy manual. Output strictly valid JSON conforming to schema."
                    )
                },
                {
                    "type": "text",
                    "text": self.STATIC_POLICY_MANUAL,
                    # Mark static policy document as cached prefix
                    "cache_control": {"type": "ephemeral"}
                }
            ],
            messages=[
                {
                    "role": "user",
                    "content": f"<audit_log>\n{sanitized_log}\n</audit_log>\nOutput valid JSON compliance evaluation."
                },
                {
                    # Prefill to force immediate JSON structure
                    "role": "assistant",
                    "content": "{\n  \"policy_id\":"
                }
            ]
        )

        # 4. Telemetry Verification
        usage = response.usage
        print(f"Cache Telemetry: Read={getattr(usage, 'cache_read_input_tokens', 0)}, "
              f"Created={getattr(usage, 'cache_creation_input_tokens', 0)}, "
              f"Output={usage.output_tokens}")

        # Reconstruct full JSON string from prefill
        full_json = "{\n  \"policy_id\":" + response.content[0].text

        # 5. Type-Safe Validation with Defensive Self-Healing
        try:
            return ComplianceEvaluation.model_validate_json(full_json)
        except ValidationError as e:
            # Self-correction fallback
            print(f"Schema validation error: {e}. Executing targeted repair...")
            repair_response = self.client.messages.create(
                model="claude-3-5-haiku-20241022",
                max_tokens=1024,
                temperature=0.0,
                messages=[
                    {"role": "user", "content": f"Fix this JSON to match schema. Error: {e}\nRaw JSON:\n{full_json}"}
                ]
            )
            return ComplianceEvaluation.model_validate_json(repair_response.content[0].text)

if __name__ == "__main__":
    compiler = EnterprisePromptCompiler()
    sample_log = "User logged in. Transferred $75,000 to offshore bank account with single signature."
    result = compiler.evaluate_audit_event(sample_log)
    print(result.model_dump_json(indent=2))
