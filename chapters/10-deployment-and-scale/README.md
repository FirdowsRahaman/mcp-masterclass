# Chapter 10: Deployment & Scale

## Objective
In 10 minutes, you will understand:
- How to transition an MCP server from local `stdio` development to production.
- Hosting MCP servers in the cloud using SSE transport.
- Scaling strategies for high-traffic MCP architectures.

## The Concept
Building an MCP server locally is easy. Deploying it to production so that thousands of distributed AI agents can query it simultaneously requires traditional web-scale engineering.

### The "Restaurant Franchise" Analogy
**Scaling an MCP Server is like moving from a Food Truck to a Restaurant Franchise.**
- A local `stdio` server is a **Food Truck**: It's simple, runs on one machine, and one person (the Host) talks directly to it.
- Scaling to the cloud (SSE) is building a **Franchise**: You need identical, containerized kitchens (Docker), someone standing outside directing customer traffic (Load Balancers), and you suddenly have to worry about people stealing the recipes (Authentication).

## How It Works

### 1. Containerization (Docker)
The first step to deployment is containerizing your server. Because FastMCP seamlessly switches to an ASGI app (like FastAPI) when using SSE, your Dockerfile looks just like a standard web app.

```dockerfile
# Example Dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY server.py .

# Expose the SSE port
EXPOSE 8000

# Run the server using an ASGI server like Uvicorn (FastMCP handles this internally when mcp.run(transport="sse") is called)
CMD ["python", "server.py"]
```

### 2. Cloud Hosting (AWS, GCP, Render)
Deploy your containerized server to a cloud provider. Because SSE maintains long-lived HTTP connections, you must ensure your load balancers are configured to support long timeouts and HTTP/2.

- **AWS**: Use ECS/Fargate with an Application Load Balancer (ALB).
- **GCP**: Use Cloud Run (ensure "Session Affinity" is enabled if state is required).

### 3. Scaling Considerations
- **Statelessness**: Try to keep your MCP servers stateless. If a server maintains local memory between the `initialize` and `tools/call` steps, a load balancer might route the second request to a different container, breaking the workflow. Use external databases (Redis, Postgres) for state.
- **Authentication**: When moving from `stdio` (implicitly secure) to `SSE` (public internet), you *must* implement authentication middleware (e.g., Bearer tokens in headers).

### 4. Professional Pattern: The Lifespan
For servers that need to manage external resources (like database connections), use the **lifespan** context manager. This ensures resources are cleanly managed during server startup and shutdown.

```python
from contextlib import asynccontextmanager

@asynccontextmanager
async def app_lifespan(server: FastMCP):
    db = await connect_to_db()
    try:
        yield {"db": db}
    finally:
        await db.close()

mcp = FastMCP("App", lifespan=app_lifespan)
```

### 5. Multi-Server Orchestration: Starlette Mounting
You can run multiple MCP servers in a single web application by mounting them into a **Starlette** (or FastAPI) app. This is perfect for complex enterprise environments.

```python
from starlette.applications import Starlette
from starlette.routing import Mount

echo_mcp = FastMCP("Echo", stateless_http=True)
math_mcp = FastMCP("Math", stateless_http=True)

app = Starlette(
    routes=[
        Mount("/echo", echo_mcp.streamable_http_app()),
        Mount("/math", math_mcp.streamable_http_app()),
    ]
)
```

### 6. Enterprise Configuration: The `env` Object
When connecting a local server to Claude Desktop, you often need to pass sensitive keys or custom paths. Always use the `env` object in your `claude_desktop_config.json` to avoid polluting your global system environment:

```json
{
  "mcpServers": {
    "my-server": {
      "command": "python",
      "args": ["server.py"],
      "env": {
        "API_KEY": "sk-...",
        "CUSTOM_PATH": "/usr/local/bin"
      }
    }
  }
}
```

### 7. Packaging with MCP Bundles (MCPB)
For easier distribution, the ecosystem is moving toward **MCP Bundles (MCPB)**. An `.mcpb` file is a standardized package that contains the server code, its dependencies, and its configuration. This allows "One-Click" installation into supporting MCP hosts.

### 8. The Reverse Bridge: Exposing ADK Tools as MCP Servers
If you have built complex reasoning tools using the **Agent Development Kit (ADK)**, you can easily expose them as standard MCP servers. This allows non-ADK applications (like Claude Desktop or Cursor) to use your ADK tools.

Using the `adk_to_mcp_tool_type` utility, you can wrap an ADK `FunctionTool` and serve it via a standard Python MCP server:

```python
from mcp.server.lowlevel import Server
from google.adk.tools.function_tool import FunctionTool
from google.adk.tools.mcp_tool.conversion_utils import adk_to_mcp_tool_type

# 1. Your existing ADK tool
def my_complex_logic(query: str):
    return f"ADK processed: {query}"

adk_tool = FunctionTool(my_complex_logic)

# 2. Create MCP Server
app = Server("adk-to-mcp-bridge")

@app.list_tools()
async def list_tools():
    # Convert ADK schema to MCP schema
    return [adk_to_mcp_tool_type(adk_tool)]

# 3. Serve over stdio
# (Standard MCP run loop follows...)
```

## Try It Yourself

Let's simulate deploying your server to the cloud using Docker.

1. Create a new directory and save the `server.py` code from Chapter 1.
2. Change the bottom line to: `mcp.run(transport="sse")`
3. Save the `Dockerfile` provided in Section 1 above into the same folder.
4. Create a `requirements.txt` file containing exactly one line: `mcp`
5. Build the container image:
   ```bash
   docker build -t my-mcp-server .
   ```
6. Run the container and map the port:
   ```bash
   docker run -p 8000:8000 my-mcp-server
   ```
7. Open the MCP Inspector (`npx @modelcontextprotocol/inspector`), choose the **SSE** transport, and connect to `http://127.0.0.1:8000/sse`. You have successfully containerized and deployed an MCP server!

## Checkpoint
1. Why does moving from `stdio` to SSE suddenly require you to think about Authentication?
2. What happens if a load balancer routes an MCP request to a different container midway through a session?
3. What is the primary benefit of exposing an ADK tool as an MCP server?
