# Project 4: Maps Grounding Agent

<div align="center">
  <img src="../../assets/maps-agent.png" alt="Maps Grounding Interface" width="100%">
</div>

This project demonstrates how to use the **Agent Development Kit (ADK)** to build an agent that is grounded in real-world geographic data using the Google Maps Grounding Lite MCP server.

## Overview
In this project, you will:
1. Enable the **Maps Grounding Lite** service on your Google Cloud Project.
2. Configure your environment with a Google Cloud API Key.
3. Use ADK's `McpToolset` to load the official Maps MCP server.
4. Build a Python agent that can answer complex location-based questions with zero hallucination.

## Setup Instructions

### 1. Google Cloud Configuration
- Navigate to the [Google Cloud Console](https://console.cloud.google.com/).
- Create a new project or select an existing one.
- Search for **"Maps Grounding Lite"** in the API Library and enable the service.
- Create an **API Key** under Credentials.

### 2. Environment Variables
Create a `.env` file in this directory and add your key:
```bash
GCP_API_KEY=your_api_key_here
```

### 3. Install Dependencies
```bash
pip install adk-python python-dotenv
```

## Running the Agent
The agent uses the `McpToolset` from ADK to connect to the Google Maps MCP server.

```bash
python agent.py
```

## What's Happening Under the Hood?
- **ADK McpToolset**: Instead of manually writing JSON-RPC handshakes, ADK's `McpToolset` automatically discovers all tools offered by the Google Maps MCP server.
- **Protocol Boundary**: The agent sends requests to the server, which then calls the Google Cloud Maps API and returns validated geographic context.
- **Grounding**: The LLM uses the returned data to ensure that addresses, distances, and location details are factually correct.
