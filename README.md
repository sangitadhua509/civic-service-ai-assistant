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

## Phase 2 — CRUD for Department, Service, Citizen

New files added:
```
app/
├── schemas/
│   ├── department.py   # DepartmentCreate / Update / Out
│   ├── service.py      # ServiceCreate / Update / Out
│   └── citizen.py      # CitizenCreate / Update / Out
├── api/
│   ├── departments.py  # /departments CRUD
│   ├── services.py     # /services CRUD
│   └── citizens.py     # /citizens CRUD
└── core/
    └── fake_db.py       # TEMPORARY in-memory storage (Phase 3 replaces this)
```

### How to run it

You already have the venv set up from Phase 1. Just pull/copy these new
files into your project, then:

```powershell
.\venv\Scripts\Activate.ps1
uvicorn app.main:app --reload
```

### How to test it (no coding needed — use Swagger UI)

1. Open **http://127.0.0.1:8000/docs**
2. You'll now see three new sections: **Departments**, **Services**, **Citizens**.
3. Try this exact sequence to see the whole flow work:
   - `POST /departments` → click "Try it out" → use the example body → Execute.
     You'll get back an object with `"id": 1`.
   - `GET /departments` → Execute → you'll see the department you just created.
   - `POST /services` → set `"department_id": 1` (matching what you just created)
     → Execute. If you use a department_id that doesn't exist, you'll correctly
     get a `400 Bad Request` — try it to see the validation in action.
   - `POST /citizens` → Execute with any `user_id` for now (auth isn't built yet).
   - `GET /services?department_id=1` → shows the department filter working.
   - `PUT /departments/1` → send just `{"description": "Updated description"}`
     → Execute → notice only that field changed, everything else stayed the same.
   - `DELETE /departments/1` → Execute → then `GET /departments/1` → you'll get
     a `404 Not Found`, confirming it's gone.

**Important:** since this is in-memory storage, if you stop the server
(Ctrl+C) and restart it, everything you created will disappear. That's
expected — this gets fixed in Phase 3 with a real PostgreSQL database.

### Concepts this phase teaches

- **Pydantic schemas** separate "what the client sends" (Create/Update)
  from "what we send back" (Out) — the client can never invent their own `id`.
- **`exclude_unset=True`** on updates means "only touch the fields the
  client actually included in the request" — this is what makes partial
  updates (PATCH-style behavior via PUT here) work correctly.
- **HTTP status codes are meaningful**: 201 for created, 204 for deleted
  (nothing to return), 404 for missing, 400 for a bad request like a
  non-existent department_id.

### Don't forget to commit

```powershell
git add .
git commit -m "Phase 2: Pydantic schemas + CRUD for Department, Service, Citizen (in-memory)"
git push
```

## Next phase

**Phase 3** replaces `fake_db.py` with a real PostgreSQL database:
SQLAlchemy models, a database session, and Alembic migrations so your
data survives restarts and the team can share one schema.

Just say "next phase" when you're ready.
