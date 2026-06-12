# Backend - Kanban Studio

## Tech Stack
- Python 3.12 with FastAPI
- Uvicorn as ASGI server
- SQLite database (added in Part 6)
- OpenAI Python SDK for OpenRouter AI calls (added in Part 8)
- `uv` as package manager

## Structure (current - Part 2)
```
backend/
  main.py         - FastAPI app with / and /api/hello endpoints
  pyproject.toml  - Python dependencies
```

## Commands (inside Docker)
- `uv run uvicorn main:app --host 0.0.0.0 --port 8000` - Start the server

## API Endpoints
- `GET /` - Serves static HTML (will serve NextJS export in Part 3)
- `GET /api/hello` - Returns `{"message": "Hello from FastAPI"}`

## Docker
- The backend runs inside a Docker container at `/app`
- Static files from the frontend build are at `/app/static`
- Port 8000 exposed
