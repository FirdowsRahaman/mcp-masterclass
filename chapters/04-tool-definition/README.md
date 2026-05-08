# Chapter 4: Tool Definition & Schemas

## Objective
In 10 minutes, you will understand:
- How to implement MCP servers using Python and TypeScript SDKs
- Server configuration and registration patterns
- Local development workflows for server testing
- Production deployment considerations

## The Concept
MCP servers act as the interface between the protocol and actual tool implementations. They handle request routing, validation, and execution while adhering to the MCP specification.

### The "Standard Operating Procedure" Analogy
**Writing an MCP Tool Schema is like writing an SOP for a new employee.**
If you just tell a brand new hire "fix the database", chaos will ensue. They don't know what database, what tools to use, or what "fix" means. 
You must give them a strict Standard Operating Procedure (SOP). 
A **JSON Schema** is the SOP for an LLM—it strictly defines the exact inputs, the expected data types, and the required outcomes so the AI doesn't hallucinate parameters.

### Core Components
- **Server Instance**: Manages protocol lifecycle
- **Tool Registry**: Catalog of available tools
- **Execution Context**: Environment for tool execution
- **Middleware Pipeline**: Request/response processing

## How It Works

### Server Architecture
```
┌─────────────────────────────────────────────────────┐
│                   MCP Server                        │
├───────────────┬───────────────────┬─────────────────┤
│  Protocol     │  Tool Registry    │  Execution      │
│  Handler      │  (Tool Catalog)   │  Environment    │
├───────────────┼───────────────────┼─────────────────┤
│  Middleware   │  Validation       │  Resource       │
│  Pipeline     │  Layer            │  Management     │
└───────────────┴───────────────────┴─────────────────┘
```

### Implementation Flow
1. **Initialize Server**: Configure name, version, capabilities
2. **Register Tools**: Define tool functions with schemas
3. **Start Server**: Begin listening for MCP connections
4. **Handle Requests**: Process incoming tool requests

### Development Workflow
- Local testing with MCP Inspector
- Hot-reload during development
- Integration with host environments

## Code Example: Defining Tools with FastMCP

With FastMCP, defining a tool is as simple as writing a standard Python function and adding the `@mcp.tool()` decorator. The SDK automatically reads your Python type hints (`str`, `int`, etc.) and your docstring, converting them into the strict JSON Schema required by the MCP protocol.

```python
from mcp.server.fastmcp import FastMCP

# FastMCP automatically handles capabilities and routing
mcp = FastMCP("file-operations")

@mcp.tool()
def read_file(path: str) -> str:
    """Read contents of a file. FastMCP infers the schema from these type hints."""
    with open(path, 'r') as f:
        return f.read()

@mcp.tool()
def write_file(path: str, content: str) -> bool:
    """Write content to a file."""
    with open(path, 'w') as f:
        f.write(content)
    return True
```

### Structured Output with Pydantic
For complex tools, returning a plain string isn't always enough. You can return **Pydantic models** to provide the AI with a strict, machine-readable structure. FastMCP will automatically generate the JSON schema for the return type.

```python
from pydantic import BaseModel

class FileMetadata(BaseModel):
    path: str
    size: int
    encoding: str

@mcp.tool()
def get_metadata(path: str) -> FileMetadata:
    """Get detailed metadata for a file."""
    return FileMetadata(path=path, size=1024, encoding="utf-8")

if __name__ == "__main__":
    # Start the server using stdio transport (standard for MCP)
    mcp.run()
```

## Try It Yourself

1. Create a new directory and file for your server:
   ```bash
   mkdir -p tool-server && cd tool-server
   touch server.py
   ```
2. Install the FastMCP SDK: 
   ```bash
   pip install mcp
   ```
3. Copy the code examples above into `server.py`.
4. Start the server via the Inspector: 
   ```bash
   npx @modelcontextprotocol/inspector python server.py
   ```
5. In the Inspector UI, click **Tools**. You should see `read_file`, `write_file`, and `get_metadata` beautifully formatted with their schemas!

## Checkpoint
1. How does FastMCP know what JSON schema to generate for a tool?
2. Why is a strict Standard Operating Procedure (JSON Schema) critical for LLMs?

## Architect Notes

### Trade-offs
- **Language Choice**: Python for rapid development vs TypeScript for type safety
- **Resource Management**: Direct access vs sandboxed execution
- **Error Handling**: Generic errors vs detailed debugging information

### Production Considerations
- Implement health checks and readiness probes
- Add request throttling and rate limiting
- Use structured logging for monitoring
- Implement graceful shutdown procedures
- Consider containerization for deployment consistency
- Design for horizontal scaling of stateless servers