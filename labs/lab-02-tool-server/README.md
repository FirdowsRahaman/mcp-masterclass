# Lab 2: Building a Tool Server

## Objective
Learn how to build practical MCP tools using complex input schemas, automatic validation, and Pydantic models.

## 🛠 Prerequisites
- Completion of Lab 1
- Python 3.10+

## Step 1: Project Setup

```bash
mkdir -p mcp-lab-02
cd mcp-lab-02
python -m venv venv
source venv/bin/activate
pip install mcp pydantic
```

## Step 2: Complex Tool Schemas with FastMCP

FastMCP automatically generates JSON Schema for your tools based on Python type hints and Pydantic models. This ensures AI models know exactly what inputs your tools require, drastically reducing hallucinations.

Create `weather_server.py`:

```python
# weather_server.py
from mcp.server.fastmcp import FastMCP
from pydantic import BaseModel, Field

mcp = FastMCP("weather-server")

# Define our complex input schema using Pydantic
class WeatherQuery(BaseModel):
    city: str = Field(description="The name of the city (e.g., 'London', 'Tokyo')")
    country_code: str | None = Field(default=None, description="Optional 2-letter ISO country code")
    units: str = Field(default="metric", description="Temperature units: 'metric' or 'imperial'")

@mcp.tool()
def get_current_weather(query: WeatherQuery) -> str:
    """
    Fetch the current weather for a given location.
    Always use this tool when the user asks for the current weather.
    """
    # In a real app, you would make an HTTP request to a weather API here.
    # For this lab, we'll return mock data.
    
    # Validation is already handled by FastMCP/Pydantic before this code runs!
    if query.units not in ["metric", "imperial"]:
        return "Error: Units must be 'metric' or 'imperial'."
        
    temp = 22 if query.units == "metric" else 72
    unit_str = "°C" if query.units == "metric" else "°F"
    
    location = f"{query.city}, {query.country_code}" if query.country_code else query.city
    
    return f"The current weather in {location} is {temp}{unit_str} and sunny."

if __name__ == "__main__":
    mcp.run()
```

## Step 3: Test Schema Validation

1. Start the Inspector:
   ```bash
   npx @modelcontextprotocol/inspector python weather_server.py
   ```
2. Open the Inspector in your browser.
3. Go to the **Tools** tab. Look at the JSON Schema generated for `get_current_weather`. Notice how the descriptions from your `Field` declarations are perfectly translated to help the AI model understand the parameters!
4. **Try breaking it:** Attempt to execute the tool *without* providing the required `city` parameter. FastMCP will automatically reject the request and return a validation error before your function even runs.

## 🎉 Success!
You now know how to design robust, type-safe tools that guide AI models toward successful execution. In Lab 3, we will add Resources to provide read-only context.
