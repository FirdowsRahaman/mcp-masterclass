import os
from google.adk.agents import Agent
from google.adk.tools.mcp_tool import McpToolset
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def main():
    api_key = os.getenv("GCP_API_KEY")
    if not api_key:
        print("Error: GCP_API_KEY not found in environment.")
        return

    # 1. Initialize the MCP Toolset for Google Maps
    # This automatically loads the official Google Maps Grounding MCP server
    maps_tools = McpToolset(
        server_url="https://github.com/google/maps-grounding-mcp",
        env={"API_KEY": api_key}
    )

    # 2. Create the Agent and attach the toolset
    agent = Agent(
        name="MapsExpert",
        instructions="You are a geographic expert. Use the provided maps tools to verify all location data.",
        tools=[maps_tools]
    )

    # 3. Ask a question that requires real-world grounding
    prompt = "What is the distance between the Eiffel Tower and the Louvre Museum? Please verify the exact coordinates."
    
    print(f"User: {prompt}\n")
    print("Agent is thinking...")
    
    response = agent.chat(prompt)
    
    print(f"\nMapsExpert: {response}")

if __name__ == "__main__":
    main()
