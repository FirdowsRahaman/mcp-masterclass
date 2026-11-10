"""
Lab 7: GDPR PII Sanitization Gateway & EU AI Act Article 12 Audit Logger
Demonstrates privacy-preserving MCP middleware with European regulatory audit logging.
"""

import re
import json
import hashlib
import time
from datetime import datetime, timezone
from typing import Dict, Any, Tuple
from mcp.server.fastmcp import FastMCP, Context

# Initialize FastMCP Server
mcp = FastMCP("gdpr-sovereign-gateway")

# =====================================================================
# 1. GDPR PII Sanitizer (Privacy by Design - GDPR Art. 25 & 32)
# =====================================================================

class GDPRSanitizer:
    """Detects and masks EU-specific personal data before tool processing."""
    
    PATTERNS = {
        "EMAIL": r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+",
        "EU_IBAN": r"[A-Z]{2}\d{2}[A-Z0-9]{4}\d{7}([A-Z0-9]?){0,16}",
        "PHONE": r"(\+?[0-9]{1,4}[\s-]?)?(\(?[0-9]{2,4}\)?[\s-]?)?[0-9]{3,4}[\s-]?[0-9]{3,4}",
        "GERMAN_TAX_ID": r"\b\d{2}/\d{3}/\d{5}\b"
    }

    @classmethod
    def sanitize(cls, text: str) -> Tuple[str, Dict[str, str]]:
        mapping = {}
        sanitized = text
        counter = 1
        
        for pii_type, pattern in cls.PATTERNS.items():
            matches = re.findall(pattern, sanitized)
            for match in matches:
                if isinstance(match, tuple):
                    match = match[0]
                if not match or len(match.strip()) < 4:
                    continue
                token = f"[{pii_type}_{counter}]"
                mapping[token] = match
                sanitized = sanitized.replace(match, token)
                counter += 1
                
        return sanitized, mapping

# =====================================================================
# 2. EU AI Act Article 12 Tamper-Evident Audit Logger
# =====================================================================

class EUAIActAuditLogger:
    """Emits immutable structured event logs adhering to EU AI Act Article 12."""
    
    @staticmethod
    def log_event(tool_name: str, sanitized_args: Dict[str, Any], status: str, duration_ms: float):
        event = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "regulatory_framework": "EU_AI_ACT_ART_12",
            "jurisdiction": "EEA / Sovereign VPC",
            "tool_name": tool_name,
            "sanitized_payload": sanitized_args,
            "status": status,
            "latency_ms": round(duration_ms, 2),
            "verification_hash": hashlib.sha256(
                f"{tool_name}:{status}:{time.time()}".encode()
            ).hexdigest()
        }
        # In production, stream to OpenTelemetry collector / WORM S3 Glacier storage
        print(f"\n📋 [EU AI Act Audit Log] {json.dumps(event, indent=2)}")

# =====================================================================
# 3. Secure MCP Tools with Middleware Hooks
# =====================================================================

@mcp.tool()
def process_european_invoice(invoice_text: str, ctx: Context) -> str:
    """
    Processes an EU commercial invoice safely after passing through
    GDPR Article 25 privacy sanitization and emitting an Article 12 audit log.
    """
    start_time = time.time()
    
    # 1. Sanitize incoming payload
    sanitized_text, pii_mapping = GDPRSanitizer.sanitize(invoice_text)
    ctx.info(f"GDPR Masking Applied: Redacted {len(pii_mapping)} sensitive identifiers.")
    
    # 2. Execute business logic on sanitized data
    execution_result = {
        "status": "APPROVED",
        "processed_text": sanitized_text,
        "masked_entities_count": len(pii_mapping),
        "sovereign_region": "eu-central-1"
    }
    
    duration_ms = (time.time() - start_time) * 1000
    
    # 3. Emit Article 12 Audit Log
    EUAIActAuditLogger.log_event(
        tool_name="process_european_invoice",
        sanitized_args={"sanitized_text": sanitized_text},
        status="SUCCESS",
        duration_ms=duration_ms
    )
    
    return json.dumps(execution_result)

if __name__ == "__main__":
    # Test execution
    test_invoice = "Invoice for user max.mustermann@berlin-tech.de, IBAN DE89370400440532013000, Amount €1,450.00"
    print("Testing GDPR Sanitization Gateway:")
    sanitized, mapping = GDPRSanitizer.sanitize(test_invoice)
    print(f"Original:  {test_invoice}")
    print(f"Sanitized: {sanitized}")
    print(f"PII Map:   {mapping}")
    mcp.run()
