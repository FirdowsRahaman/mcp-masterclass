# Lab 6: Multi-Server Agent Orchestration

## Objective
Connect to multiple MCP servers simultaneously from a single Client script, demonstrating how agents orchestrate across domain boundaries.

## 🛠 Prerequisites
- You need the Python scripts from Lab 1 (`server.py`) and Lab 3 (`kb_server.py`).

## Step 1: Project Setup

```bash
mkdir -p mcp-lab-06
cd mcp-lab-06
python -m venv venv
source venv/bin/activate
# We need the low-level mcp package to act as a client
pip install mcp
```

Copy your `server.py` from Lab 1 and rename it to `hello_server.py` in this folder.
Create an empty database file for the SQLite server: `touch test.db`

## Step 2: Build the Orchestrator Client

The true power of MCP is composability. A host (like Claude Desktop or your own custom agent) can connect to dozens of servers simultaneously over `stdio` subprocesses, aggregating their capabilities.

Create `orchestrator.py`:

```python
# orchestrator.py
import asyncio
from contextlib import AsyncExitStack
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

class OrchestratorClient:
    def __init__(self):
        self.exit_stack = AsyncExitStack()
        self.sessions: dict[str, ClientSession] = {}

    async def add_server(self, name: str, command: str, args: list[str]):
        server_params = StdioServerParameters(command=command, args=args)
        transport = await self.exit_stack.enter_async_context(stdio_client(server_params))
        read, write = transport
        session = await self.exit_stack.enter_async_context(ClientSession(read, write))
        await session.initialize()
        self.sessions[name] = session
        print(f"Connected to {name}")

    async def cleanup(self):
        await self.exit_stack.aclose()

async def main():
    orchestrator = OrchestratorClient()
    try:
        print("Booting servers...")
        # Server 1: Custom Python Server
        await orchestrator.add_server("hello-mcp", "python", ["hello_server.py"])
        # Server 2: Official Node.js SQLite Server
        await orchestrator.add_server("sqlite", "npx", ["-y", "@modelcontextprotocol/server-sqlite", "test.db"])
        
        # 1. Aggregate Capabilities
        print("\n--- Aggregated Tool Catalog ---")
        for name, session in orchestrator.sessions.items():
            response = await session.list_tools()
            for tool in response.tools:
                print(f"[{name}] offers Tool: {tool.name}")
                
        # 2. Execute Action on Server 1
        print("\n--- Executing Cross-Domain Actions ---")
        hello_session = orchestrator.sessions["hello-mcp"]
        result = await hello_session.call_tool("say_hello", {"name": "Orchestrator"})
        print(f"Hello Server Result: {result.content[0].text}")

    finally:
        await orchestrator.cleanup()

if __name__ == "__main__":
    asyncio.run(main())
```

## Step 3: Run the Orchestrator

Execute the client script:
```bash
python orchestrator.py
```

You should see the client boot up both servers sequentially, aggregate their tools and resources, and then successfully execute commands against both independent servers.

## 🎉 Success!
You've built a multi-server orchestrator! This is exactly how production systems like Claude Desktop aggregate local file system tools, database tools, and web search tools into a single, cohesive AI context. 

Congratulations on completing the MCP Masterclass Labs!
