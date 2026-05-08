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
