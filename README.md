# Agent Memory Playground

A hands-on project for exploring and comparing modern memory agent frameworks, including [mem0](https://github.com/mem0ai/mem0) and [Google ADK Memory](https://github.com/google/adk). This repo provides working examples, local development scripts, and integration with vector stores and LLMs for building memory-augmented agents.

---

## Features

- **mem0**: Open-source memory agent with Qdrant vector store and Ollama embedding support
- **Google ADK Memory**: Google’s Agent Development Kit with memory tools and LLM integration
- **Qdrant**: Local vector database for fast memory retrieval
- **Ollama**: Local embedding and LLM serving
- Example scripts for both mem0 and Google ADK memory
- Docker Compose for local infrastructure

---

## Quick Start

### 1. Prerequisites
- Python 3.12+
- Docker (for Qdrant and Ollama)

### 2. Clone and Install
```bash
git clone <this-repo-url>
cd agent_memory
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt  # or use pyproject.toml with your tool
```

### 3. Start Local Services
```bash
docker compose up -d
```
This launches Qdrant (vector DB) and Ollama (embeddings/LLM) locally.

### 4. Run Example Scripts

#### mem0 Example
```bash
python scripts/local_memory.py
```

#### Google ADK Memory Example
```bash
python scripts/adk_memory.py
```

---

## Project Structure

- `src/agent_memory/` – Main app code and config
- `scripts/local_memory.py` – mem0 local memory demo
- `scripts/adk_memory.py` – Google ADK memory agent demo
- `docker-compose.yml` – Qdrant and Ollama services
- `localdev/volumes/` – Data volumes for Qdrant/Ollama

---

## Configuration

- **Vector Store**: Qdrant (localhost:6333)
- **Embeddings**: Ollama (`nomic-embed-text:latest` by default)
- **LLM**: OpenAI (default: `gpt-5-nano`), configurable in scripts

You can adjust model names and ports in the scripts and `docker-compose.yml`.

---

## References
- [mem0](https://github.com/mem0ai/mem0)
- [Google ADK](https://github.com/google/adk)
- [Qdrant](https://qdrant.tech/)
- [Ollama](https://ollama.com/)

---

## License
MIT
