# Lab 7: GDPR PII Sanitization Gateway & EU AI Act Audit Logger 

This lab implements an enterprise-grade **Model Context Protocol (MCP)** gateway that:
1. Automatically intercepts tool parameters to redact **GDPR personal identifiers** (European IBANs, passport numbers, email addresses, phone numbers) before tool execution.
2. Emits an immutable, structured audit log fulfilling **EU AI Act Article 12 (Record-Keeping & Traceability)** requirements.

---

## Learning Objectives

- Implement an MCP middleware wrapper that sanitizes tool inputs using GDPR privacy-by-design principles.
- Preserve de-identification mapping in an encrypted, isolated memory session for downstream deanonymization.
- Generate OpenTelemetry-compatible JSON-L audit events recording caller identity, tool name, execution latency, and deterministic verification hashes.

---

## Architecture

```
Agent Tool Request ──▶ [GDPR PII Scrubbing Middleware]
                               │
            (IBAN, Email, Name replaced with Tokens)
                               │
                               ▼
                       [Secure Tool Execution]
                               │
                               ▼
            [EU AI Act Article 12 Audit Logger (OpenTelemetry)]
                               │
                               ▼
                    Tool Output to Agent
```

---

## Running the Server

```bash
python server.py
```
