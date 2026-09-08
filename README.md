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

## Phase 3 — Real PostgreSQL database + Alembic migrations

New files added:
```
app/
├── db/
│   ├── base_class.py    # the SQLAlchemy Base class
│   ├── base.py           # imports every model (Alembic reads this)
│   ├── session.py        # engine, SessionLocal, get_db()
│   └── models/
│       ├── user.py       # User table (login comes in Phase 4)
│       ├── department.py
│       ├── service.py    # requirements stored as JSONB
│       └── citizen.py    # address stored as JSONB
alembic/
├── env.py                # wires Alembic to our settings + models
├── script.py.mako        # template for new migration files
└── versions/              # generated migration files land here
alembic.ini                 # Alembic configuration
scripts/
└── seed_sample_data.py    # inserts fictional departments/services/users
```

`app/core/fake_db.py` is now DELETED — `departments.py`, `services.py`,
and `citizens.py` were rewritten to use the real database. The URL
paths, request/response shapes, and status codes are all unchanged —
only the storage underneath changed.

### 1. Install PostgreSQL (one-time, outside Python)

1. Download from **postgresql.org/download/windows** → run the installer.
2. Keep the default components checked. Set a **superuser password**
   and write it down. Keep port `5432`.
3. Open **pgAdmin 4** (installed alongside Postgres) → expand
   **Servers → PostgreSQL 16** (enter your password) → right-click
   **Databases → Create → Database…** → name it `civic_db` → Save.

### 2. Update your .env file

Open `.env` (not `.env.example`) and set your real password:
```
DATABASE_URL=postgresql+psycopg2://postgres:YOUR_PASSWORD@localhost:5432/civic_db
```

### 3. Install the new Python packages

```powershell
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

### 4. Generate and run your first migration

This is the moment Alembic looks at your model files and writes the
actual SQL needed to create matching tables:

```powershell
alembic revision --autogenerate -m "create initial tables"
alembic upgrade head
```

- The first command creates a new file in `alembic/versions/` — open
  it and skim it, you'll see it's just readable Python describing
  "create table users...", "create table departments...", etc.
- The second command actually runs that SQL against your `civic_db`
  database.

If this succeeds, open pgAdmin → civic_db → Schemas → public → Tables
— you should now see `users`, `departments`, `services`, `citizens`.

### 5. Seed fictional sample data

```powershell
python scripts/seed_sample_data.py
```

This prints out the ids it created — note the citizen user id, you'll
need it for testing.

### 6. Run the server and test persistence

```powershell
uvicorn app.main:app --reload
```

Go to `/docs` and try:
- `GET /departments` → you should see the two seeded departments already there.
- `POST /citizens` with the `user_id` the seed script printed for the sample citizen.
- **Now actually stop the server (Ctrl+C) and start it again.** Run
  `GET /departments` again — your data is still there. That's the
  entire point of Phase 3: no more disappearing data.
- Try `POST /services` with a `department_id` that doesn't exist (e.g. `999`)
  — you should get a 400, now enforced by PostgreSQL's foreign key
  constraint rather than manual code.

### Concepts this phase teaches

- **ORM (Object-Relational Mapping)** — SQLAlchemy models let you work
  with database rows as normal Python objects (`department.name`)
  instead of writing raw SQL everywhere.
- **Foreign keys** — `ForeignKey("departments.id")` makes the database
  itself refuse invalid references, instead of your code checking manually.
- **Migrations** — Alembic tracks every schema change as a numbered,
  reversible file, so your teammates (and your final submission) can
  rebuild the exact same database structure from an empty one.
- **JSONB** — flexible nested data (documents list, address) stored in
  a single column, used for `Service.requirements` and `Citizen.address`.

### Don't forget to commit

```powershell
git add .
git commit -m "Phase 3: PostgreSQL database, SQLAlchemy models, Alembic migrations, seed data"
git push
```

## Next phase

**Phase 4** adds real authentication: password hashing, `/auth/register`
and `/auth/login` endpoints, JWT tokens, and role-based permission
checks (admin / officer / citizen) so routes actually get protected.

Just say "next phase" when you're ready.
