# Civic Service AI Assistant — Phase 1 (Project Setup)

This is Phase 1 of the capstone: a bare FastAPI app with one working
health-check endpoint. No database, no auth yet — that comes in later
phases. The goal here is just: **get a Python web server running on
your machine.**

## What's inside

```
civic-service-ai-assistant/
├── requirements.txt      # list of Python packages this project needs
├── .env.example          # template for secret settings (copy -> .env)
├── .gitignore            # tells Git which files NOT to commit
├── README.md             # this file
└── app/
    ├── main.py           # the FastAPI app itself — starts here
    ├── core/
    │   ├── config.py     # reads settings from .env
    │   └── logging.py    # sets up readable log messages
    └── api/
        └── health.py     # the /health endpoint
```

## Step-by-step setup (copy-paste these, in order)

### 1. Make sure you have Python 3.11+ installed
Check with:
```bash
python3 --version
```

### 2. Create a virtual environment
This creates an isolated folder for this project's packages only.
```bash
python3 -m venv venv
```

### 3. Activate it
- **Mac/Linux:**
  ```bash
  source venv/bin/activate
  ```
- **Windows (PowerShell):**
  ```powershell
  venv\Scripts\Activate.ps1
  ```
You'll know it worked because your terminal prompt will now show `(venv)` at the start.

### 4. Install the dependencies
```bash
pip install -r requirements.txt
```

### 5. Create your real .env file
```bash
cp .env.example .env
```
(On Windows: `copy .env.example .env`)
You don't need to edit it yet — the defaults work fine for Phase 1.

### 6. Run the server
```bash
uvicorn app.main:app --reload
```

If it worked, you'll see something like:
```
INFO:     Uvicorn running on http://127.0.0.1:8000
```

### 7. Check it in your browser
- Open **http://127.0.0.1:8000/** → you should see a welcome JSON message.
- Open **http://127.0.0.1:8000/health** → you should see `{"status": "ok", ...}`.
- Open **http://127.0.0.1:8000/docs** → this is Swagger UI, FastAPI's
  auto-generated interactive API documentation. You'll use this constantly
  from Phase 2 onwards to test endpoints without writing any request code.

## What each file is actually doing (plain English)

- **`app/main.py`** — creates the FastAPI app and tells it which sets of
  endpoints ("routers") to include. Right now only `health` is plugged in.
  As we build more features, each one gets its own file and gets added
  here with one line.
- **`app/core/config.py`** — reads your `.env` file into a Python object
  called `settings`, so any file can do `from app.core.config import settings`
  and get e.g. `settings.APP_NAME` instead of hard-coding values.
- **`app/core/logging.py`** — makes log output readable (timestamp, level,
  message) instead of scattered `print()` statements.
- **`app/api/health.py`** — one endpoint, `/health`, whose only job is to
  say "I'm alive." Used later by Docker/monitoring to check the app is up.

## Next phase

**Phase 2** adds Pydantic schemas and the first real CRUD endpoints
(Department, Service, Citizen) — still without a database, using
temporary in-memory storage, so you can understand request/response
validation before we bring PostgreSQL into the picture.

Just say "next phase" when you're ready and I'll build it the same way.
