import asyncio

from google.adk.agents import LlmAgent
from google.adk.models.lite_llm import LiteLlm
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types
from mem0 import Memory

# Initialize Mem0 client
config = {
    "vector_store": {
        "provider": "qdrant",
        "config": {
            "collection_name": "test",
            "host": "localhost",
            "port": 6333,
            "embedding_model_dims": 768,  # Change this according to your local model's dimensions
        },
    },
    "llm": {
        "provider": "openai",
        "config": {
            "model": "gpt-5-nano",
            "temperature": 0.1,
            "max_tokens": 2000,
        },
    },
    "embedder": {
        "provider": "ollama",
        "config": {
            "model": "nomic-embed-text:latest",
            # Alternatively, you can use "snowflake-arctic-embed:latest"
            "ollama_base_url": "http://localhost:11434",
        },
    },
}


# Initialize Memory with the configuration
memory = Memory.from_config(config)


# Define memory function tools
def search_memory(query: str, user_id: str) -> dict:
    """Search through past conversations and memories"""
    # For Platform API, user_id goes in filters
    filters = {"user_id": user_id}
    memories = memory.search(query, filters=filters)
    if memories.get("results", []):
        memory_list = memories["results"]
        memory_context = "\n".join([f"- {mem['memory']}" for mem in memory_list])
        return {"status": "success", "memories": memory_context}
    return {"status": "no_memories", "message": "No relevant memories found"}


def save_memory(content: str, user_id: str) -> dict:
    """Save important information to memory"""
    try:
        result = memory.add([{"role": "user", "content": content}], user_id=user_id)
        return {
            "status": "success",
            "message": "Information saved to memory",
            "result": result,
        }
    except Exception as e:
        return {"status": "error", "message": f"Failed to save memory: {str(e)}"}


# Create agent with memory capabilities
personal_assistant = LlmAgent(
    name="personal_assistant",
    model=LiteLlm(model="openai/gpt-5-nano"),  # LiteLLM model string format,
    instruction="""You are a helpful personal assistant with memory capabilities.
    Use the search_memory function to recall past conversations and user preferences.
    Use the save_memory function to store important information about the user.
    Always personalize your responses based on available memory.""",
    description="A personal assistant that remembers user preferences and past interactions",
    tools=[search_memory, save_memory],
)


async def chat_with_agent(user_input: str, user_id: str) -> str:
    """
    Handle user input with automatic memory integration.

    Args:
        user_input: The user's message
        user_id: Unique identifier for the user

    Returns:
        The agent's response
    """
    # Set up session and runner
    session_service = InMemorySessionService()
    session = await session_service.create_session(
        app_name="memory_assistant", user_id=user_id, session_id=f"session_{user_id}"
    )
    runner = Runner(
        agent=personal_assistant,
        app_name="memory_assistant",
        session_service=session_service,
    )

    # Create content and run agent
    content = types.Content(role="user", parts=[types.Part(text=user_input)])
    events = runner.run(user_id=user_id, session_id=session.id, new_message=content)

    # Extract final response
    for event in events:
        if event.is_final_response():
            response = event.content.parts[0].text  # type: ignore

            return response  # type: ignore

    return "No response generated"


# Example usage
if __name__ == "__main__":
    response = asyncio.run(
        chat_with_agent(
            "I love Italian food and I'm planning a trip to Rome next month",
            user_id="alice",
        )
    )
    print(response)
