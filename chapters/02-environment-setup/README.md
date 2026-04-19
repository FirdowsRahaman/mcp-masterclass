# Chapter 2: Environment Setup & Host Environment

## Objective
In 10 minutes, you will understand:
- Different MCP host environments (Claude Desktop, Cursor, Custom Host)
- How MCP Inspector works for protocol debugging
- Local vs remote execution models
- Runtime requirements for MCP compatibility

## The Concept
MCP requires a host environment that manages the communication between AI models and tool servers. The host acts as the orchestrator of the protocol lifecycle.

### The "Workshop" Analogy
**Setting up an MCP environment is like setting up a Workshop.**
You don't just build furniture (AI responses) out on the grass. You need a structured environment:
- **The Workshop (The Host)**: The building itself (Claude Desktop, Cursor) that provides security, power, and space.
- **The Workbench (Docker/Runtime)**: The specific table where the work happens.
- **The Power Tools (MCP SDKs/Servers)**: The specialized equipment (File system reader, SQL executor) plugged into the workbench.

### Core Components
- **Host**: Runtime environment that executes the protocol
- **Inspector**: Debugging tool for visualizing protocol flow
- **Runtime**: Execution context for tool servers

## How It Works

### Host Comparison Matrix
| Host | Type | Debugging | Customization | Production Ready |
|------|------|-----------|---------------|------------------|
| Claude Desktop | Native | Limited | Low | ✅ |
| Cursor | IDE Plugin | Medium | Medium | ✅ |
| Custom Host | Self-built | Full | High | ✅ |

### MCP Inspector Workflow
1. **Capture**: Intercept MCP protocol traffic
2. **Visualize**: Display handshake sequence and messages
3. **Debug**: Inspect request/response payloads
4. **Replay**: Test modifications to protocol flow

### Execution Models
- **Local Execution**: Tool servers run on same machine as host
- **Remote Execution**: Tool servers run on separate infrastructure
- **Hybrid Model**: Mix of local and remote servers

### Code Example
> [!NOTE]
> *This example uses conceptual pseudo-code (`MCPHost`) to illustrate host responsibilities. In reality, a host is often a full application like Claude Desktop, not a single python class.*

```python
# Custom MCP Host Implementation
from mcp.host import MCPHost

host = MCPHost(
    name="Custom Enterprise Host",
    version="1.0",
    capabilities={
        "tool_execution": True,
        "state_management": "persistent",
        "security": "zero-trust"
    }
)

# Connect to local tool server
host.register_server("http://localhost:8000")

# Start host runtime
host.start()
```

## Try It Yourself

1. Install MCP Inspector
2. Start a local tool server (from Chapter 1)
3. Connect to it via:
   ```bash
   mcp-inspector --connect http://localhost:8000
   ```
4. Execute a tool call and observe:
   - Handshake sequence
   - Request/response structure
   - State management behavior

## Checkpoint
1. What are three key differences between Claude Desktop and a Custom Host?
2. When would you choose remote execution over local execution?

## Architect Notes

### Trade-offs
- **Debugging Depth**: Custom hosts offer more visibility but require more setup
- **Performance**: Local execution has lower latency but limited scalability
- **Security**: Remote execution requires additional network security layers

### Production Considerations
- Implement host health monitoring for protocol stability
- Design for host version compatibility
- Consider network topology for remote execution
- Use MCP Inspector in staging environments for protocol validation
- Plan for graceful degradation when tool servers are unavailable