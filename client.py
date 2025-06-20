import asyncio
import os
from dotenv import load_dotenv
from langchain_mcp_adapters.client import MultiServerMCPClient
from langgraph.prebuilt import create_react_agent
from langchain_google_genai import ChatGoogleGenerativeAI  # or use ChatGroq

load_dotenv()

async def main():
    client = MultiServerMCPClient(
        {
            "math": {
                "command": "python",
                "args": ["math_Server.py"],  # ✅ Use absolute path
                "transport": "stdio",
            },
            "weather": {
                "url": "http://localhost:8000/mcp",
                "transport": "streamable_http",
            }
        }
    )

    # Get tool schemas from MCP servers
    tools = await client.get_tools()

    # Instantiate your LLM (make sure your .env contains GOOGLE_API_KEY)
    llm = ChatGoogleGenerativeAI(model='gemini-1.5-pro')

    # Create a ReAct agent using LangGraph
    agent = create_react_agent(llm, tools)

    # Query the agent
    result = await agent.ainvoke({
        "messages": [  # ✅ Use "messages" instead of "message"
            {
                "role": "user",
                "content": "what is (3*4) * 4 ?"
            }
        ]
    })

    # Print the response
    print("math response:", result['messages'][-1].content)

# Run the async main function
if __name__ == "__main__":
    print("this is good")
    asyncio.run(main())
