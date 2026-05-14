# Lab 3: Building a Resource Server

## Objective
Learn the crucial distinction between Tools (actions) and Resources (context). You will implement a dynamic Resource Server that provides read-only data for AI models to use as context.

## Tools vs. Resources Refresher
- **Tools**: Actions the model *chooses* to execute (e.g., `calculate_sum`, `write_file`).
- **Resources**: Read-only data the application or user *provides* to the model as context (e.g., `file://logs.txt`, `database://schema`).

## Step 1: Project Setup

```bash
mkdir -p mcp-lab-03
cd mcp-lab-03
python -m venv venv
source venv/bin/activate
pip install mcp
```

## Step 2: Implementing Resources

We will build a "Knowledge Base" server that provides internal company documentation as resources. 

Create `kb_server.py`:

```python
# kb_server.py
from mcp.server.fastmcp import FastMCP
import asyncio

mcp = FastMCP("knowledge-base")

# Mock database
KNOWLEDGE_DB = {
    "onboarding": "Welcome! Please set up your laptop and read the security guidelines.",
    "security": "Never share your password. Always lock your screen.",
    "architecture": "We use a microservices architecture built on Kubernetes."
}

# 1. Define a static resource
@mcp.resource("kb://index")
async def get_index() -> str:
    """
    List of all available knowledge base topics.
    The LLM reads this description to understand what data it will get.
    """
    await asyncio.sleep(0.1) # Simulate network delay
    return "Available topics: " + ", ".join(KNOWLEDGE_DB.keys())

# 2. Define a dynamic resource using URI templates
@mcp.resource("kb://topic/{topic_name}")
async def get_topic(topic_name: str) -> str:
    """
    Read a specific knowledge base topic.
    Provides detailed internal company documentation.
    """
    await asyncio.sleep(0.1) # Simulate database lookup
    
    if topic_name not in KNOWLEDGE_DB:
        return f"Error: Topic '{topic_name}' not found."
    
    return KNOWLEDGE_DB[topic_name]

if __name__ == "__main__":
    mcp.run()
```

## Step 3: Inspecting Resources

1. Start the Inspector:
   ```bash
   npx @modelcontextprotocol/inspector python kb_server.py
   ```
2. Open the Inspector in your browser.
3. Navigate to the **Resources** tab (not the Tools tab!).
4. You will see the static resource `kb://index` and a template for `kb://topic/{topic_name}`.
5. Click to read the `kb://index` resource. The server will return the content.
6. Try filling in the template with `kb://topic/security` and reading it. 

## 🎉 Success!
You've implemented the Resource pattern! In a real application like Claude Desktop, the user can attach these URIs to their conversation, injecting massive amounts of precise context directly into the prompt without forcing the model to "use a tool" to find it.
