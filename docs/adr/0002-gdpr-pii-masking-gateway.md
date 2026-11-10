# 2. Client-Side GDPR PII Masking Gateway

Date: 2026-02-05

## Status
Accepted

## Context
Under GDPR Article 5(1)(c) (Data Minimization) and Article 25 (Data Protection by Design), personal identifiers such as IBANs, tax IDs, and email addresses must not be dispatched to external tools or LLM providers without strict legal justification.

## Decision
We implement a deterministic PII sanitization middleware that intercepts all tool inputs, replaces personal identifiers with cryptographic tokens (e.g., `[EU_IBAN_1]`), and only re-identifies data within secure, auditable egress points.

## Consequences
- Guarantees compliance with European GDPR standards.
- Minimizes risk of confidential corporate or personal data leakage.
