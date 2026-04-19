# Chapter 4: Building MCP Servers

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

### Code Example
```python
# Chapter 4: Tool Definitionation (Python)
from mcp.server.fastmcp import FastMCP

# FastMCP automatically handles capabilities and routing
mcp = FastMCP("file-operations")

@mcp.tool()
def read_file(path: str) -> str:
    """Read contents of a file. FastMCP automatically infers the schema from these type hints."""
    with open(path, 'r') as f:
        return f.read()

@mcp.tool()
def write_file(path: str, content: str) -> bool:
    """Write content to a file."""
    with open(path, 'w') as f:
        f.write(content)
    return True

if __name__ == "__main__":
    # Start the server using stdio transport (standard for MCP)
    mcp.run()
```

## Try It Yourself

1. Create a new directory for your server:
   ```bash
   mkdir -p labs/lab-02-tool-server/server
   cd labs/lab-02-tool-server/server
   ```
2. Initialize a Python virtual environment
3. Install MCP SDK: `pip install mcp-sdk`
4. Create `server.py` with the code example above
5. Start the server: `python server.py`
6. Connect using MCP Inspector and test file operations

## Checkpoint
1. What are the key differences between dev_mode and production mode?
2. How does the server handle tool validation before execution?

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