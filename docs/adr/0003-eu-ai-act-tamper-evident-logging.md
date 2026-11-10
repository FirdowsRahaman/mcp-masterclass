# 3. Tamper-Evident Audit Logging for EU AI Act Article 12

Date: 2026-02-18

## Status
Accepted

## Context
Regulation (EU) 2024/1689 (EU AI Act) Article 12 mandates that high-risk AI system gateways must automatically record all interactions to enable post-market monitoring and regulatory auditability.

## Decision
All MCP tool calls must emit an immutable structured log containing timestamp, caller ID, sanitized payload, latency, and a SHA-256 verification hash, streamed to WORM-compliant cloud storage.

## Consequences
- Produces verifiable, audit-ready compliance evidence for European regulatory bodies.
- Overhead: negligible latency addition (< 2ms) per tool call.
