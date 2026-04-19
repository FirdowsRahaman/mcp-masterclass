# Chapter 8: Prompts & Templates

## Objective
In 10 minutes, you will understand:
- The third core primitive of MCP: **Prompts**
- How servers can define reusable, parameterized prompt templates
- How to "trick" the LLM into using tools more accurately via structured prompt instructions

## The Concept
While Tools are for *actions* and Resources are for *data*, Prompts are for **instruction**. MCP allows a Server to define a catalog of reusable Prompts. 

### The "Bureaucratic Form" Analogy
**An MCP Prompt is a Mad Libs form for AI.**
Imagine trying to get a building permit by writing a free-form essay to the city council. It would be a disaster. Instead, the government hands you a strict form with blanks to fill out.
Similarly, instead of letting users write chaotic, free-form instructions for complex tasks, the MCP server provides a structured template (the Prompt). The user fills in the blanks (`language`, `strictness`), which guarantees the LLM receives the exact same, highly-optimized instruction set every single time.

## How It Works

### The Prompt Primitive
A Prompt defined on the server includes:
- A `name` and `description` (for discovery)
- A list of `arguments` (the blanks to fill in)
- The returning `messages` (the actual instructions sent to the LLM)

This is incredibly powerful for standardizing complex workflows, like "Code Review" or "Incident Response", ensuring the LLM always follows the exact same chain of thought.

### Code Example
```python
from mcp.server.fastmcp import FastMCP
from mcp.types import PromptMessage, TextContent

mcp = FastMCP("prompt-server")

@mcp.prompt()
def review_code(language: str, strictness: str = "high") -> list[PromptMessage]:
    """A standardized prompt template for reviewing code."""
    
    instruction = f"""
    You are an expert {language} developer. Please review the provided code.
    Your strictness level is set to: {strictness}.
    
    Please ensure you:
    1. Check for security vulnerabilities
    2. Check for performance bottlenecks
    3. Ensure PEP-8/standard formatting
    """
    
    return [
        PromptMessage(
            role="user",
            content=TextContent(type="text", text=instruction)
        )
    ]
```

## Try It Yourself
1. Implement the `review_code` prompt above.
2. Run your server using the MCP Inspector.
3. Navigate to the **Prompts** tab.
4. Fill in the `language` argument and click "Get Prompt". 
5. Notice how the server constructs the precise message structure that the AI model will eventually receive!

## Checkpoint
1. What is the fundamental difference between an MCP Tool and an MCP Prompt?
2. Why would you host a Prompt on an MCP server instead of just typing it into the AI chat interface manually?
