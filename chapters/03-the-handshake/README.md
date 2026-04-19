# Chapter 3: The Handshake & Handshake

## Objective
In 10 minutes, you will understand:
- The complete MCP protocol lifecycle phases
- Handshake sequence and message structure
- State management patterns (stateless vs stateful)
- How to debug protocol flow using MCP Inspector

## The Concept
MCP follows a well-defined lifecycle for every interaction. To understand the exact order of operations and "who calls whom," it helps to think of a restaurant.

### The "Restaurant" Analogy
**The MCP Handshake is like ordering food at a restaurant.**
- **The Initialization (Reading the Menu)**: The MCP Client (Waiter) connects to the Server (Kitchen) and asks "What can you do?" The Server replies with its Capabilities (The Menu).
- **The Execution (Placing the Order)**: The AI Agent (Customer) decides it wants a specific tool. The Client (Waiter) takes this exact JSON-RPC order to the Server (Kitchen).
- **The Result (Serving the Food)**: The Server executes the Python code and hands the raw data back to the Client, which serves it to the Agent.

### Core Lifecycle Phases
1. **Initialize**: Establish connection parameters
2. **Capabilities**: Exchange feature support
3. **Tool Discovery**: Server advertises available tools
4. **Execution**: Request/response for tool operations
5. **Teardown**: Clean connection closure

## How It Works

### Protocol Sequence Diagram
```
Client                Host                Server
 |                    |                    |
 |-- Initialize ------>|                    |
 |<----- Ready --------|                    |
 |       |            |-- Capabilities --->|
 |       |            |<-- Capabilities ---|
 |       |            |-- Tool Discovery ->|
 |       |            |<-- Tool Catalog ----|
 |------- Tool Request ------------------->|
 |<------ Tool Response ------------------|
 |                    |                    |
```

### Message Structure
```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "method": "tools/call",
  "params": {
    "name": "calculator.add",
    "arguments": {
      "a": 5,
      "b": 7
    }
  }
}
```

### State Management Patterns
| Pattern | Description | Use Case |
|---------|-------------|----------|
| Stateless | No context maintained between requests | Simple tool calls |
| Ephemeral | Context maintained per session | Multi-turn interactions |
| Persistent | Context stored externally | Long-running workflows |

## Code Example
```python
# Protocol Lifecycle Implementation
async def handle_handshake(client):
    # Initialize phase
    init = await client.receive()
    if init["type"] != "initialize":
        await client.send({"error": "Invalid handshake"})
        return

    # Capabilities exchange
    await client.send({"type": "ready"})
    capabilities = await client.receive()
    
    # Tool discovery
    tool_catalog = server.get_tool_catalog()
    await client.send({"type": "tool_catalog", "payload": tool_catalog})

    # Main execution loop
    while True:
        request = await client.receive()
        if request["type"] == "tool_request":
            response = await execute_tool(request)
            await client.send(response)
```

## Try It Yourself

1. Start MCP Inspector
2. Run the Chapter 1 calculator server
3. Initiate a tool request and observe:
   - Handshake sequence in Inspector
   - Message structure details
   - Context propagation between requests
4. Modify the server to use persistent state and observe changes

## Checkpoint
1. What happens if capabilities negotiation fails during handshake?
2. How does context differ from state in MCP messages?

## Architect Notes

### Trade-offs
- **State Management**: Persistent state increases complexity but enables advanced workflows
- **Message Size**: Context payloads can grow large; implement pruning strategies
- **Error Recovery**: Design for resumable sessions after connection drops

### Production Considerations
- Implement message validation at each lifecycle phase
- Add timeouts for each protocol phase
- Monitor handshake success rates for integration health
- Use message IDs for request tracing and deduplication
- Plan for protocol version compatibility across components