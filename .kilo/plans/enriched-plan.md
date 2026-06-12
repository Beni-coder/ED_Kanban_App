# Plan - Kanban Studio MVP

## Overview

Build a full-stack Kanban board app: NextJS frontend (static export) served by a Python FastAPI backend, packaged in Docker, with AI-powered chat sidebar via OpenRouter.

---

## Part 1: Plan (current phase)

### Substeps
- [x] Review existing frontend code structure
- [x] Enrich PLAN.md with detailed substeps, tests, and success criteria
- [ ] Create `frontend/AGENTS.md` describing the existing frontend code
- [ ] Get user sign-off on the enriched plan

### Tests & Success Criteria
- User approves the enriched plan before moving to Part 2

---

## Part 2: Scaffolding - Docker + FastAPI + Hello World

### Substeps
- [ ] Create `backend/main.py` with a minimal FastAPI app:
  - `GET /` serves a static HTML file ("Hello World")
  - `GET /api/hello` returns a JSON response `{"message": "Hello from FastAPI"}`
- [ ] Create `backend/pyproject.toml` with dependencies: `fastapi`, `uvicorn`, `python-dotenv`
- [ ] Configure NextJS for static export (`output: "export"` in `next.config.ts`)
- [ ] Create `Dockerfile` at project root:
  - Stage 1: Node - build the NextJS static export into `frontend/out/`
  - Stage 2: Python (using `uv`) - install backend deps, copy static files into a directory served by FastAPI
  - Expose port 8000
  - CMD: `uvicorn main:app --host 0.0.0.0 --port 8000`
- [ ] Create `docker-compose.yml` that loads `.env` and maps port 8000
- [ ] Create start/stop scripts in `scripts/`:
  - `start.bat` (Windows), `start.sh` (Mac/Linux): `docker compose up --build`
  - `stop.bat` (Windows), `stop.sh` (Mac/Linux): `docker compose down`
- [ ] Update `backend/AGENTS.md` and `scripts/AGENTS.md`
- [ ] Update `frontend/AGENTS.md` to reflect static export changes

### Tests
- [ ] `docker compose up --build` succeeds without errors
- [ ] `GET http://localhost:8000/` returns HTML with "Hello World"
- [ ] `GET http://localhost:8000/api/hello` returns `{"message": "Hello from FastAPI"}`
- [ ] Start and stop scripts work on target platform

### Success Criteria
- Docker container builds and runs
- Both the static page and API endpoint are reachable at localhost:8000

---

## Part 3: Serve the Frontend via FastAPI

### Substeps
- [ ] Update FastAPI to serve the NextJS static export from `frontend/out/` at `/`
  - Use `StaticFiles` middleware for static assets
  - Ensure `index.html` is served at `/`
- [ ] Ensure the Dockerfile properly builds the frontend and copies output to the right location
- [ ] Verify the Kanban board renders correctly when served from FastAPI
- [ ] Translate all user-facing strings in the frontend to French:
  - Column headers, button labels, placeholder text, header text
  - Keep variable names and technical strings in English

### Tests
- [ ] `GET http://localhost:8000/` shows the full Kanban board with all 5 columns
- [ ] All 8 demo cards are visible
- [ ] Existing unit tests still pass: `npm run test:unit` (run outside Docker)
- [ ] Existing e2e tests pass (adjusted for port 8000)

### Success Criteria
- Kanban board renders at `/` with all demo data
- All French translations applied
- All existing tests pass

---

## Part 4: Fake User Sign-In

### Substeps
- [ ] Add `POST /api/login` endpoint accepting `username` and `password`
  - Returns a session token (simple hardcoded check: `"user"` / `"password"`)
  - Token stored in an in-memory set on the backend
- [ ] Add `POST /api/logout` endpoint
- [ ] Add auth middleware: unauthenticated requests to `/api/board` redirect or return 401
- [ ] Add `GET /api/me` endpoint returning current user info (or 401 if not logged in)
- [ ] Create a `LoginPage` component in the frontend:
  - Simple form with username/password fields
  - On submit, calls `POST /api/login`
  - Stores session token (cookie or localStorage)
- [ ] Add auth state management in the frontend:
  - On app load, check `GET /api/me`
  - If authenticated, show Kanban board
  - If not, show login page
- [ ] Add a logout button to the Kanban header
- [ ] Translate all sign-in UI to French

### Tests
- [ ] Unit test: `POST /api/login` with correct credentials returns 200 + token
- [ ] Unit test: `POST /api/login` with wrong credentials returns 401
- [ ] Unit test: `GET /api/me` with valid token returns user info
- [ ] Unit test: `GET /api/me` without token returns 401
- [ ] Unit test: `POST /api/logout` clears session
- [ ] Frontend test: login page renders with French labels
- [ ] Frontend test: successful login shows Kanban board
- [ ] Frontend test: logout returns to login page
- [ ] E2E test: full login flow works in browser

### Success Criteria
- Hitting `/` without being logged in shows the login form
- Logging in with "user"/"password" shows the Kanban board
- Logging out returns to the login form
- All text is in French

---

## Part 5: Database Modeling

### Substeps
- [ ] Design SQLite schema with the following tables:
  - `users` (id, username, password_hash) - for future multi-user support
  - `boards` (id, user_id, title)
  - `columns` (id, board_id, title, position)
  - `cards` (id, column_id, title, details, position)
- [ ] Save schema as `docs/database-schema.json` and `docs/database.md`
- [ ] Add `aiichat` table for conversation history:
  - `chat_messages` (id, user_id, role, content, created_at)
- [ ] Get user sign-off on the schema

### Tests & Success Criteria
- User approves the schema before proceeding

---

## Part 6: Backend API for Kanban CRUD

### Substeps
- [ ] Add SQLite database initialization in `backend/`:
  - Create DB file if it doesn't exist
  - Run schema migrations on startup
  - Seed with default user ("user"/"password") and default board with 5 columns + demo cards
- [ ] Add `backend/database.py` module for DB connection and initialization
- [ ] Add CRUD API routes (all protected by auth):
  - `GET /api/board` - returns full board data (columns + cards) for the logged-in user
  - `PUT /api/columns/{id}` - rename a column
  - `POST /api/cards` - create a card in a column
  - `PUT /api/cards/{id}` - edit card title/details
  - `DELETE /api/cards/{id}` - delete a card
  - `PUT /api/cards/{id}/move` - move a card to a different column/position
- [ ] Add `backend/tests/` with pytest-based unit tests for each endpoint
- [ ] Update `backend/AGENTS.md`

### Tests
- [ ] Unit test: DB initializes with default user and board
- [ ] Unit test: `GET /api/board` returns seeded data
- [ ] Unit test: rename column persists
- [ ] Unit test: create/read/update/delete card works
- [ ] Unit test: move card between columns works
- [ ] Unit test: unauthenticated requests return 401

### Success Criteria
- All CRUD operations work via API
- Data persists across server restarts (SQLite)
- All backend tests pass

---

## Part 7: Frontend + Backend Integration

### Substeps
- [ ] Replace frontend's `initialData` with a fetch to `GET /api/board`
- [ ] Wire up column rename to `PUT /api/columns/{id}`
- [ ] Wire up card creation to `POST /api/cards`
- [ ] Wire up card deletion to `DELETE /api/cards/{id}`
- [ ] Wire up card move (drag-and-drop) to `PUT /api/cards/{id}/move`
- [ ] Add optimistic UI updates with error rollback
- [ ] Add loading states for initial board fetch

### Tests
- [ ] E2E: board loads from API (not hardcoded data)
- [ ] E2E: rename column persists after page reload
- [ ] E2E: add a card, reload page, card still exists
- [ ] E2E: delete a card, reload page, card is gone
- [ ] E2E: drag card to another column, reload, card is in new column
- [ ] Unit tests for API fetch logic

### Success Criteria
- Kanban board is fully persistent via the backend
- All operations survive page refresh
- No hardcoded demo data remains in the frontend

---

## Part 8: AI Connectivity

### Substeps
- [ ] Add `openai` Python package to backend dependencies (for OpenRouter API calls)
- [ ] Create `backend/ai.py` module:
  - Initialize OpenAI client pointing to OpenRouter base URL
  - Read `OPENROUTER_API_KEY` from `.env`
  - Use model `openai/gpt-oss-120b`
- [ ] Add `POST /api/ai/test` endpoint that sends "What is 2+2?" and returns the response
- [ ] Test that the AI call works within Docker

### Tests
- [ ] Backend unit test: `POST /api/ai/test` returns a response containing "4" (or similar)

### Success Criteria
- Backend successfully calls OpenRouter API and returns a response
- API key is read from `.env` (not hardcoded)

---

## Part 9: AI Chat with Kanban Context

### Substeps
- [ ] Design the system prompt that includes the current Kanban board JSON
- [ ] Design the structured output schema for AI responses:
  ```json
  {
    "message": "string - response to the user",
    "actions": [
      { "type": "create_card", "column_id": "...", "title": "...", "details": "..." },
      { "type": "edit_card", "card_id": "...", "title": "...", "details": "..." },
      { "type": "move_card", "card_id": "...", "column_id": "...", "position": 0 },
      { "type": "delete_card", "card_id": "..." }
    ]
  }
  ```
- [ ] Implement `POST /api/ai/chat`:
  - Loads the user's current board state
  - Loads conversation history from `chat_messages` table
  - Sends system prompt + board JSON + conversation history + user message to AI
  - Parses structured output
  - Executes any Kanban actions on the database
  - Saves user message and AI response to `chat_messages`
  - Returns AI message + list of actions taken
- [ ] Add backend tests with mocked AI responses

### Tests
- [ ] Unit test: chat endpoint saves messages to DB
- [ ] Unit test: AI response with "create_card" action creates a card in DB
- [ ] Unit test: AI response with "move_card" action moves a card in DB
- [ ] Unit test: AI response with "edit_card" action updates a card in DB
- [ ] Unit test: AI response with "delete_card" action removes a card from DB
- [ ] Unit test: conversation history is maintained across calls

### Success Criteria
- Chat endpoint returns AI responses and correctly applies board mutations
- All actions are tested with mocked AI

---

## Part 10: AI Chat Sidebar UI

### Substeps
- [ ] Create `ChatSidebar` component:
  - Toggle button to open/close sidebar (fixed position)
  - Chat message list with user/AI bubbles
  - Input field + send button at the bottom
  - Loading indicator while AI is responding
- [ ] Add sidebar to the main `KanbanBoard` layout (right side, collapsible)
- [ ] Wire chat input to `POST /api/ai/chat`
- [ ] After AI response, if actions were taken, refresh the board from `GET /api/board`
- [ ] Show visual indication of AI actions (e.g., "Card created in Backlog")
- [ ] Style with the project color scheme
- [ ] Translate all chat UI strings to French
- [ ] Responsive design: sidebar overlays on smaller screens

### Tests
- [ ] Unit test: ChatSidebar renders with input and send button
- [ ] Unit test: typing and sending a message calls the API
- [ ] Unit test: AI response appears in the chat
- [ ] E2E: open sidebar, send a message, see response
- [ ] E2E: AI creates a card, board refreshes with new card visible

### Success Criteria
- Chat sidebar is visually polished and matches project color scheme
- AI chat works end-to-end
- Board updates automatically when AI makes changes
- All text in French

---

## Key Technical Notes

- **Frontend**: NextJS 16, React 19, Tailwind CSS 4, dnd-kit for drag-and-drop, Vitest for unit tests, Playwright for e2e
- **Backend**: Python FastAPI, uvicorn, SQLite, OpenAI Python SDK (pointing to OpenRouter)
- **AI**: OpenRouter API, model `openai/gpt-oss-120b`, structured outputs
- **Infra**: Docker multi-stage build (Node build -> Python serve), docker-compose, start/stop scripts
- **Language**: All user-facing text in French
- **Auth**: Simple session token (hardcoded user/password for MVP)
