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
| Claude Desktop | Native | Limited | Low |  |
| Cursor | IDE Plugin | Medium | Medium |  |
| Custom Host | Self-built | Full | High |  |

### MCP Inspector Workflow
1. **Capture**: Intercept MCP protocol traffic
2. **Visualize**: Display handshake sequence and messages
3. **Debug**: Inspect request/response payloads
4. **Replay**: Test modifications to protocol flow

### Execution Models
- **Local Execution**: Tool servers run on same machine as host
- **Remote Execution**: Tool servers run on separate infrastructure
- **Hybrid Model**: Mix of local and remote servers

### Code Example: Configuring a Host

Most developers don't write custom hosts from scratch. Instead, they plug their MCP Servers into existing robust hosts like **Claude Desktop** or **Cursor**.

Here is how you configure Claude Desktop to act as the Host for the Calculator server from Chapter 1:

**`claude_desktop_config.json`**
```json
{
  "mcpServers": {
    "calculator-server": {
      "command": "python",
      "args": [
        "/absolute/path/to/server.py"
      ]
    }
  }
}
```
*When Claude Desktop starts, it will read this config, spawn your Python process, and manage the lifecycle of the connection over standard input/output (stdio).*

### Configuring Other Popular Hosts

Because MCP is a universal standard (like "USB-C for AI"), you aren't locked into Claude Desktop. You can plug the exact same `server.py` into other powerful developer tools:

**1. Cursor (IDE)**
Cursor has native built-in MCP support for its AI chat and composer.
- Open Cursor Settings.
- Navigate to **Features** -> **MCP**.
- Click **+ Add New MCP Server**.
- Set Type to `command`, Name to `calculator`, and Command to `python /absolute/path/to/server.py`.

**2. VS Code (via Cline)**
If you use the popular [Cline](https://github.com/cline/cline) extension in VS Code, you can easily attach MCP servers to it.
- Open the Cline configuration file located at `~/Library/Application Support/Code/User/globalStorage/saoudrizwan.claude-dev/settings/cline_mcp_settings.json` (Mac).
- Add the exact same JSON structure used in the Claude Desktop configuration above.

**3. Antigravity & Advanced Agents**
Advanced autonomous agents (like Antigravity) can seamlessly connect to MCP servers. These systems often connect dynamically via the MCP Client SDKs, or they read from a global `mcp_settings.json` file to arm themselves with your custom tools and resources on the fly.

## Try It Yourself

Let's connect your Chapter 1 server to a real Host (Claude Desktop).

1. Ensure you have [Claude Desktop](https://claude.ai/download) installed.
2. Locate the configuration file (create it if it doesn't exist):
   - **Mac**: `~/Library/Application Support/Claude/claude_desktop_config.json`
   - **Windows**: `%APPDATA%\Claude\claude_desktop_config.json`
3. Edit the file to point to the absolute path of your `server.py` from Chapter 1.
4. Completely restart Claude Desktop.
5. Open a new chat and ask Claude: *"What tools do you have available?"* or *"Can you add 542 and 987 using the calculator?"*
6. Observe how the Host (Claude Desktop) discovers the tool and uses it seamlessly.

## Checkpoint
1. What are three key differences between Claude Desktop and a Custom Host?
2. When would you choose remote execution over local execution?

## Architect Notes

### Trade-offs
- **Debugging Depth**: Custom hosts offer more visibility but require more setup
- **Performance**: Local execution has lower latency but limited scalability
- **Security**: Remote execution requires additional network security layers

### Production Considerations
- Implement host health monitoring for protocol stability.
- **Pro Debugging**: In Claude Desktop, you can enable **Chrome DevTools** for deep inspection of message payloads. Create a `developer_settings.json` file in the config directory with `{"allowDevTools": true}` and press `Cmd+Option+I` (Mac) or `Ctrl+Alt+I` (Windows).
- Use MCP Inspector in staging environments for protocol validation.
- Plan for graceful degradation when tool servers are unavailable.