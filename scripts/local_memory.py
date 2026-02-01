from mem0 import Memory

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
            # "model": "gpt-4.1-nano-2025-04-14",
            # "model": "gpt-4.1-nano",
            # "model": "gpt-4.1-mini",
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
    # "graph_store": {
    #     "provider": "memgraph",
    #     "config": {
    #         "url": "bolt://localhost:7687",
    #         "username": "memgraph",
    #         "password": "your-password",
    #     },
    # },
}

# Initialize Memory with the configuration
agent_memory = Memory.from_config(config)

if __name__ == "__main__":
    # Clear previous memories for a clean slate
    agent_memory.delete_all(user_id="Alex")
    # Add a memory
    messages = [
        {"role": "user", "content": "Hi, I'm Alex. I love basketball and gaming."},
        {"role": "assistant", "content": "Hey Alex! I'll remember your interests."},
    ]
    result = agent_memory.add(messages, user_id="Alex")
    print(f"Added memory: {result}")
    print("-" * 40)
    # Retrieve memories
    memories = agent_memory.get_all(user_id="Alex")
    print(f"\nMemories for user 'Alex': {memories}")
