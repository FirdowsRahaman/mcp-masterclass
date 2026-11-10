# EU AI Act Technical Documentation (MCP Gateway)

**Regulation Reference**: Regulation (EU) 2024/1689 (EU AI Act)  
**System**: Model Context Protocol (MCP) Enterprise Gateway & Tool Control Plane  
**Classification**: High-Risk System Gateway (Article 6 & Annex III)  
**Version**: 1.0.0  

---

## 1. Scope & Objective
This documentation outlines conformity measures for the Model Context Protocol (MCP) server architecture connecting autonomous agent models to enterprise systems within the European Union (EEA).

## 2. Article 12: Automated Record-Keeping & Traceability
1. **Event Logs**: Every tool handshake, parameter verification, execution event, and response is recorded in an immutable format.
2. **Cryptographic Integrity**: Log payloads are hashed with SHA-256 and archived to WORM (Write Once, Read Many) cloud storage.
3. **Data Residency**: All audit logs are maintained within AWS `eu-central-1` (Frankfurt) or equivalent EU sovereign infrastructure.

## 3. Article 14: Human Oversight & Emergency Stop
1. **Interactive Human Approval**: High-impact actions require an explicit human confirmation challenge before tool dispatch.
2. **Kill-Switch**: The MCP server supports dynamic protocol disconnection terminating active connections in < 250ms.

## 4. Article 15: Cybersecurity & Input Validation
1. **Zero-Trust Access**: Tools require authenticated token bearer validation.
2. **Schema Enforcement**: Tool inputs are validated strictly against Pydantic / JSON Schema contracts; non-conforming types are rejected prior to execution.
3. **GDPR PII Scrubbing**: PII identifiers (IBANs, emails, phone numbers) are masked using deterministic tokens before external tool processing.
