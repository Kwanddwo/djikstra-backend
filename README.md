# Whenever you import something new

Don't forget to put it in requirements.txt! That's important for deployment.
Virtual environments will need that file to install dependencies, which is way better than using global libraries

# File Structure
```
/app
├── main.py               # FastAPI app entrypoint (creates app, includes routers)
├── config.py             # Pydantic settings for env vars (INFERENCE_URL, MCP_ENDPOINT, DB_URL…)
│
├── routers               # Thin HTTP interface layer
│   ├── ai_chat.py        # POST /ai-chat  → calls inference + MCP + moderation
│   ├── courses.py        # GET /courses, GET /courses/{id}
│   ├── lessons.py        # GET /lessons/{id}
│   ├── progress.py       # POST /user-progress, GET /user-progress
│   └── auth.py           # POST /login, POST /signup, POST /refresh-token
│
├── services              # Business logic + external integrations
│   ├── inference.py      # HTTPX wrapper for Heroku AI inference calls (with timeouts/retries)
│   ├── mcp_client.py     # HTTPX wrapper for MCP memory read/write
│   ├── moderation.py     # profanity + OpenAI-style moderation checks
│   ├── auth_service.py   # JWT creation/validation, password hashing
│   └── user_context.py   # Combines DB state into a “user summary” for prompts or MCP
│
├── models                # SQLAlchemy (or Tortoise) ORM models
│   ├── user.py
│   ├── course.py
│   ├── lesson.py
│   ├── problem.py
│   ├── progress.py
│   └── token.py          # refresh tokens, blacklists, etc.
│
├── schemas               # Pydantic request/response models
│   ├── ai.py             # ChatRequest, ChatResponse
│   ├── course.py
│   ├── lesson.py
│   ├── user.py
│   ├── auth.py           # LoginIn, TokenOut
│   └── progress.py
│
├── db                    # Database setup & CRUD helpers
│   ├── session.py        # engine/sessionmaker
│   ├── base.py           # Base class for models
│   └── crud.py           # Generic CRUD functions
│
├── utils                 # Misc helpers
│   ├── security.py       # JWT utilities, OAuth2 deps
│   └── logger.py         # Structured logging setup
│
└── tests                 # pytest tests
    ├── conftest.py
    ├── test_ai.py
    ├── test_auth.py
    └── test_progress.py

# top-level
├── Procfile               # `web: uvicorn app.main:app …`
├── requirements.txt       # fastapi, uvicorn, httpx, sqlalchemy, jose, better-profanity…
├── runtime.txt            # python-3.13.5
└── README.md              # Overview + local/Heroku dev instructions

```
