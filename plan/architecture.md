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


# V1 ARCHITECTURE

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


# V1 FILE EDITING ARCHITECTURE

There are 3 editing strategies:

| Strategy               | Difficulty | Reliability |
| ---------------------- | ---------- | ----------- |
| Full rewrite           | easy       | bad         |
| Search/replace patches | medium     | good        |
| AST-aware editing      | hard       | excellent   |

We are using:
**search/replace patch editing**.

This is realistic and production-worthy.

```
User Request
   ↓
Planner
   ↓
Retrieve Relevant File
   ↓
LLM Generates Patch
   ↓
Patch Validator
   ↓
Apply Edit
   ↓
Save Backup
```