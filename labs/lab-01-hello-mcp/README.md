# Lab 1: Hello MCP

## Objective
Set up your local development environment, build your first Model Context Protocol server using FastMCP, and test it using the official MCP Inspector.

## 🛠 Prerequisites
- Python 3.10 or higher
- A terminal or command prompt

## Step 1: Environment Setup

First, let's create an isolated Python environment and install the required packages.

```bash
# Create a new directory for this lab
mkdir -p mcp-lab-01
cd mcp-lab-01

# Create and activate a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install the official MCP SDK framework
pip install mcp
```

## Step 2: Build the Server

Create a new file named `server.py` in your lab directory.

```python
# server.py
from mcp.server.fastmcp import FastMCP

# Initialize the server
mcp = FastMCP("hello-mcp")

# Define a tool using the decorator
@mcp.tool()
def say_hello(name: str) -> str:
    """A simple tool that says hello to a user."""
    return f"Hello, {name}! Welcome to the Model Context Protocol."

if __name__ == "__main__":
    # Run the server on standard input/output (stdio)
    mcp.run()
```

## Step 3: Run and Inspect

Instead of running the Python script directly, we will use the **MCP Inspector**. The Inspector acts as an MCP Client (like Claude Desktop would), connecting to your server so you can test it visually.

Run the following command in your terminal:

```bash
npx @modelcontextprotocol/inspector python server.py
```

### Verification
1. Open your web browser to the URL provided by the Inspector (usually `http://localhost:5173`).
2. You will see the Inspector dashboard. Click **Connect**.
3. Navigate to the **Tools** tab. You should see your `say_hello` tool listed.
4. Fill in the `name` argument and click **Run Tool**.
5. You should see the successful JSON-RPC response returned by your server!

## 🎉 Success!
You've just built and tested your first MCP server. You understand how the host executes the server script and communicates with it over `stdio`. In Lab 2, we will build more complex tools with schemas.
