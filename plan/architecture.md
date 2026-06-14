The Product
# 🚀 Mini Cursor — Agentic Coding Assistant

Core idea:

```
User Goal
   ↓
AI understands project
   ↓
AI plans changes
   ↓
AI retrieves context
   ↓
AI edits files
   ↓
AI validates execution
   ↓
AI iterates until done
```

This is NOT:

autocomplete
chatbot

This is:

### a stateful orchestration system.

That distinction matters a LOT.


# OUR V1 ARCHITECTURE

```
User
  ↓
FastAPI Backend
  ↓
LangGraph Orchestrator
  ↓
Tools Layer
   ├── File Tools
   ├── Terminal Tools
   ├── Search Tools
   └── Retrieval Tools
  ↓
LLM (Ollama)
  ↓
Vector DB (later)
```