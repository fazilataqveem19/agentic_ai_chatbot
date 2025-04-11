# Import necessary modules to load environment variables from .env file
from dotenv import load_dotenv
import os

# Step 1: Load environment variables from .env file
load_dotenv()

# Now you can access the API keys
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Step 2: Setup LLM & Tools
from langchain_groq import ChatGroq
from langchain_openai import ChatOpenAI
from langchain_community.tools.tavily_search import TavilySearchResults

# Step 3: Setup AI Agent with search tool functionality
from langgraph.prebuilt import create_react_agent
from langchain_core.messages.ai import AIMessage

def get_response_from_ai_agent(llm_id, query, allow_search, system_prompt, provider):
    # Select model based on provider
    if provider == "Groq":
        llm = ChatGroq(model=llm_id)
    elif provider == "OpenAI":
        llm = ChatOpenAI(model=llm_id)
    else:
        raise ValueError("Unsupported provider")

    # Conditionally enable tools
    tools = [TavilySearchResults(max_results=2)] if allow_search else []

    # Create the AI agent
    agent = create_react_agent(
        model=llm,
        tools=tools,
        state_modifier=system_prompt
    )

    # Prepare state
    state = {"messages": query}

    # Get response from agent
    response = agent.invoke(state)
    messages = response.get("messages", [])

    # Extract last AI message content
    ai_messages = [message.content for message in messages if isinstance(message, AIMessage)]

    return ai_messages[-1] 
