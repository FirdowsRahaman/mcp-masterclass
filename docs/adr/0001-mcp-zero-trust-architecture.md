# 1. Zero-Trust Architecture for MCP Tool Execution

Date: 2026-01-20

## Status
Accepted

## Context
Exposing internal enterprise systems, databases, and APIs to autonomous LLM agents via Model Context Protocol (MCP) creates severe security risks (prompt injection, tool misuse, lateral movement).

## Decision
We enforce a Zero-Trust architecture on all MCP tools:
1. Every tool must explicitly declare its risk tier (`READ_ONLY`, `LOW`, `HIGH`).
2. Tools with side-effects require authenticated bearer credentials and human confirmation.
3. Network access is isolated by default.

## Consequences
- Prevents autonomous agents from executing destructive actions without explicit authorization.
- Fulfills EU AI Act Article 15 cybersecurity requirements.
