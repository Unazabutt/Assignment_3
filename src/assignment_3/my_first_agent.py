from agents import (
    Agent,
    Runner,
    set_default_openai_client,
    AsyncOpenAI,
    set_tracing_disabled,
    set_default_openai_api
)
import os
from dotenv import load_dotenv

load_dotenv()
external_client = AsyncOpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
   base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

set_default_openai_client(external_client)
set_tracing_disabled(True)
set_default_openai_api("chat_completions")


def start():
    dispatcher = Agent(
        name="Dispatcher",
        instructions="""
        You are Dispatcher, a helpful and friendly financial assistant for truck drivers.
        You help users categorize their load, calculate miles, and provide route mapping tips.
        Your responses should consider the current weather and market conditions.
        Never suggest routes with loads less than $1000, and avoid giving long routes.
        Always support drivers with better options and time management.
        After each interaction, summarize the driver's requirements in a written format.
        Save the report in 'output.md' located at the project root.
        """,
        model="gemini-2.0-flash"
    )

    # Example Interaction
    result = Runner.run_sync(dispatcher, """
    I need to transport a load worth $1500 from Dallas to New York.
    The distance is 1500 miles. Weather forecast indicates mild conditions across the route.
    Can you suggest the best route considering the current market demand and conditions?
    """)

    # Output result
    print(result.final_output)

    # Save to readme.md
    with open("README.md", "w") as f:
        f.write(result.final_output)