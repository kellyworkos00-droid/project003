# OpenERP-MVP (Odoo-like) — Starter

This is a minimal, runnable MVP for an extensible, Odoo-like ERP platform. It focuses on a clean, modular backend (Flask + SQLAlchemy) and a tiny static frontend to demonstrate end-to-end functionality. The first modules implement Contacts and Deals (CRM pipeline).

## Vision
- Modular, app-based ERP with a stable core and plug-in modules
- API-first: clean REST endpoints with OpenAPI docs
- Extensible domain models with shared DB base and migrations
- Simple local dev (SQLite), production-ready path (PostgreSQL)
- Secure-by-default foundations (JWT/authN/authZ roadmap)

## MVP Scope
- Backend service (Flask)
- Contacts + Deals modules with CRUD
- SQLite for development
- Minimal HTML page to list and create contacts
- Tests for the Contacts API

## Quickstart

Prereqs: Python 3.10+ recommended.

1) Create and activate a virtual environment:

```powershell
cd ./backend
python -m venv .venv
. .venv/Scripts/Activate.ps1
```

2) Install dependencies:

```powershell
pip install -r requirements.txt
```

3) Run the API server:

```powershell
python -m app.main
```

- API base: http://127.0.0.1:8000
- Contacts endpoints under `/contacts`
- Deals endpoints under `/deals`

4) Open the minimal UI:
- Simply open `frontend/index.html` in your browser
- It will call `http://127.0.0.1:8000/contacts`

5) Run tests:

```powershell
pytest -q
```

### Database migrations (Alembic)

This repo includes Alembic for schema migrations. Dev convenience still auto-creates tables; for real workflows, use Alembic:

```powershell
cd ./backend
. .venv/Scripts/Activate.ps1
alembic upgrade head
```

If you already created `data/app.db` by running the app earlier, either delete it before running migrations or stamp the current head:

```powershell
alembic stamp head
```

### Admin UI (Next.js)

```powershell
cd ./admin
npm install
copy .env.local.example .env.local
npm run dev
```

Open http://localhost:3000 — login uses backend `/auth/login` (default admin/admin; configure via `ADMIN_USERNAME`/`ADMIN_PASSWORD`).

## Roadmap (Next)
- Authentication: JWT-based login, users, roles, permissions
- Postgres + Alembic migrations
- Additional modules: Sales, Inventory, Invoicing, Projects
- UI app (React/Next.js) with module-aware navigation
- Plugin framework: dynamic discovery/registration of modules
- Multi-tenancy and audit logs
- Import/export and data tooling

## Notes
This repo is a foundation, not a finished product. The goal is to give you a working baseline and a clear path to grow into a powerful, Odoo-class system.