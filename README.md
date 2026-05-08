# MCP Masterclass
A comprehensive, end-to-end curriculum for mastering the Model Context Protocol (MCP). 

The Model Context Protocol is an open standard that allows AI models to securely connect to external tools and datasets. This repository takes you from high-level architecture down to production-grade deployment, teaching you how to build robust, secure, and scalable MCP servers using Python and the FastMCP SDK.

## The Anatomy of an AI Agent
Before building MCP servers, it's crucial to understand where MCP fits into the broader AI ecosystem. In the MCP ecosystem, there are three primary **Participants**:

1. **MCP Host**: The AI application (like Claude Desktop, Cursor, or your own custom app) that orchestrates the entire experience.
2. **MCP Client**: A component inside the Host that maintains the connection to servers and manages capability negotiation.
3. **MCP Server**: The service (what you will build) that provides tools, resources, and context to the Client.

As shown below, a production-grade AI Agent is a complex, multi-layered architecture:

<div align="center">
  <img src="assets/mcp-ecosystem.png" alt="MCP Ecosystem & Architecture" width="100%">
</div>

The architecture consists of several key layers:
- **Context & Input (Top)**: The user interface and raw inputs.
- **Agent Orchestration (Center)**: The core loop (The **Host** logic).
- **Memory System (Left)**: Context windows and vector stores.
- **Control & Governance (Right)**: Security boundaries and the **MCP Client**.
- **Model Layer**: The reasoning engine.
- **Tooling & Execution (Bottom)**: The **MCP Servers** providing external capabilities.

**The MCP Layer** acts as the strict protocol boundary between the Agent Orchestration layer and the Bottom Tooling layer, ensuring all tool routing and validation is securely standardized.

## Prerequisites
If you are only reading the theoretical **Chapters**, no installation is required! However, to participate in the hands-on **Labs** and **Projects**, please ensure you have the following:
- **Python 3.10+** installed on your system.
- **Dependencies**: Install the core toolkit via `pip install -r requirements.txt`.
- **API Key**: An API Key from an LLM provider (e.g., Anthropic, OpenAI) for testing agents.
- **MCP Inspector**: A debugging UI for testing your servers. Run it via `npx @modelcontextprotocol/inspector`.

## How to Use This Guide
This masterclass is designed to be highly practical. We recommend the following approach:
1. **Read the Theory**: Start with the `chapters/` to understand the mental models and architectural decisions.
2. **Execute the Labs**: Immediately after reading a chapter, navigate to the `labs/` directory to build the concepts locally.
3. **Build the Projects**: Once you've completed the Builder level, tackle the Capstone `projects/` to see how enterprise micro-servers orchestrate together.

## Learning Path
- **Level 1: Foundations** (Chapters 1–3) - The Big Picture, Environment Setup, Handshake
- **Level 2: Builder** (Chapters 4–6) - Tool Definition, Resource Management, Transport Layer
- **Level 3: Architect** (Chapters 7–12) - Security, Prompts, Integrations, Scale, Orchestration, Advanced Patterns

## Quick Start
1. Navigate to the first lab: `cd labs/lab-01-hello-mcp`
2. Run your server using the Inspector: `npx @modelcontextprotocol/inspector python server.py`

## Chapters
- [Chapter 1: The Big Picture](chapters/01-the-big-picture/README.md)
- [Chapter 2: Environment Setup](chapters/02-environment-setup/README.md)
- [Chapter 3: The Handshake](chapters/03-the-handshake/README.md)
- [Chapter 4: Tool Definition](chapters/04-tool-definition/README.md)
- [Chapter 5: Resource Management](chapters/05-resource-management/README.md)
- [Chapter 6: The Transport Layer](chapters/06-the-transport-layer/README.md)
- [Chapter 7: Security & Auth](chapters/07-security-and-auth/README.md)
- [Chapter 8: Prompts & Templates](chapters/08-prompts-and-templates/README.md)
- [Chapter 9: Real-World Integration](chapters/09-real-world-integration/README.md)
- [Chapter 10: Deployment & Scale](chapters/10-deployment-and-scale/README.md)
- [Chapter 11: Client & Orchestration](chapters/11-client-and-orchestration/README.md)
- [Chapter 12: Advanced Architecture](chapters/12-advanced-mastery/README.md)

## Labs
- [Lab 1: Run MCP locally](labs/lab-01-hello-mcp/README.md)
- [Lab 2: Build a tool server](labs/lab-02-tool-server/README.md)
- [Lab 3: Add resource context](labs/lab-03-resource-server/README.md)
- [Lab 4: Prompts & Templates](labs/lab-04-prompts-and-templates/README.md)
- [Lab 5: Add security layer](labs/lab-05-secure-tools/README.md)
- [Lab 6: Multi-server orchestration](labs/lab-06-multi-server-agent/README.md)

## Projects
- [AI Dev Assistant](projects/ai-dev-assistant/README.md) - GitHub + Code tools, Fix bugs automatically
- [Clinical Copilot](projects/clinical-copilot/README.md) - Patient data → diagnosis tools, Safe tool execution
- [Data Agent](projects/data-agent/README.md) - BigQuery / SQL tools, Analytics via MCP
- [Maps Grounding Agent](projects/maps-grounding-agent/README.md) - Google Cloud Maps integration using ADK McpToolset

## Recommended Ecosystem Tools
To get the most out of MCP, we highly recommend integrating with these powerful ecosystem tools:
- **[LangChain](https://www.langchain.com/)**: The industry standard framework for building context-aware reasoning applications. Perfect for acting as the Orchestrator/Client for your MCP servers.
- **[Agent Development Kit (ADK)](https://adk.dev/)**: An essential toolkit for rapidly developing, testing, and deploying intelligent agents that consume MCP tools.

Created by [Firdows Rahaman](https://github.com/FirdowsRahaman)