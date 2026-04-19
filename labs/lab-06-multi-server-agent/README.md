# Lab 6: Multi-Server Agent Orchestration

## Objective
Connect to multiple MCP servers simultaneously from a single Client script, demonstrating how agents orchestrate across domain boundaries.

## 🛠 Prerequisites
- You need the Python scripts from Lab 1 (`server.py`) and Lab 3 (`kb_server.py`).

## Step 1: Project Setup

```bash
mkdir -p mcp-lab-05
cd mcp-lab-05
python -m venv venv
source venv/bin/activate
# We need the low-level mcp package to act as a client
pip install mcp
```

Copy your `server.py` from Lab 1 and rename it to `hello_server.py` in this folder.
Copy your `kb_server.py` from Lab 3 into this folder.

## Step 2: Build the Orchestrator Client

The true power of MCP is composability. A host (like Claude Desktop or your own custom agent) can connect to dozens of servers simultaneously over `stdio` subprocesses, aggregating their capabilities.

Create `orchestrator.py`:

```python
# orchestrator.py
import asyncio
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

async def main():
    # Define parameters to launch the two servers as subprocesses
    server1_params = StdioServerParameters(command="python", args=["hello_server.py"])
    server2_params = StdioServerParameters(command="python", args=["kb_server.py"])

    print("Orchestrator: Connecting to Server 1 (Hello)...")
    async with stdio_client(server1_params) as (read1, write1):
        async with ClientSession(read1, write1) as session1:
            await session1.initialize()
            
            print("Orchestrator: Connecting to Server 2 (Knowledge Base)...")
            async with stdio_client(server2_params) as (read2, write2):
                async with ClientSession(read2, write2) as session2:
                    await session2.initialize()
                    
                    # 1. Aggregate Capabilities
                    print("\n--- Aggregated Tool Catalog ---")
                    tools = await session1.list_tools()
                    for tool in tools.tools:
                        print(f"Server 1 offers Tool: {tool.name}")
                        
                    # 2. Aggregate Resources
                    print("\n--- Aggregated Resource Catalog ---")
                    resources = await session2.list_resources()
                    for res in resources.resources:
                        print(f"Server 2 offers Resource: {res.uri}")
                    
                    # 3. Execute across domains
                    print("\n--- Executing Cross-Domain Actions ---")
                    # Call tool on Server 1
                    hello_result = await session1.call_tool("say_hello", {"name": "Orchestrator"})
                    print(f"Server 1 Result: {hello_result.content[0].text}")
                    
                    # Read resource from Server 2
                    kb_result = await session2.read_resource("kb://topic/security")
                    print(f"Server 2 Result: {kb_result.contents[0].text}")

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
