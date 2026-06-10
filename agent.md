# Agent Guide

## Project Overview

Luminara is a Django + Vue project.

- Backend: Django 6.0.6
- Admin UI: django-simpleui
- Frontend: Vue 3 + Vite
- Database: SQLite at `db.sqlite3`
- Django app: `core`
- Django project package: `luminara`

The public frontend is served by Vue. Django still handles `/admin/` and can be extended later for APIs.

## Key Paths

- `manage.py`: Django command entrypoint.
- `luminara/settings.py`: Django settings.
- `luminara/urls.py`: URL routing. `/admin/` is Django admin; `/` and SPA paths serve Vue.
- `core/views.py`: Serves the built Vue `index.html`.
- `frontend/`: Vue source project.
- `frontend/src/App.vue`: Main Vue page.
- `frontend/vite.config.js`: Vite config; builds into `static/frontend`.
- `static/frontend/`: Built Vue assets served by Django.
- `requirements.txt`: Python dependencies.

## Environment

Use the local virtual environment:

```powershell
Set-ExecutionPolicy -ExecutionPolicy Bypass -Scope Process -Force
. .\.venv\Scripts\Activate.ps1
```

If PowerShell blocks npm scripts, use `npm.cmd` instead of `npm`.

## Windows / Codex Runtime Troubleshooting

These are environment issues observed in Codex Desktop / managed PowerShell sessions. They do not usually indicate a project code problem.

### `Start-Process` Fails With `Path` / `PATH`

Symptom:

```text
Start-Process : An item with the same key has already been added. Key: Path / PATH
```

Cause: Windows environment variables are case-insensitive, but some process environments may contain both `Path` and `PATH`. PowerShell / .NET can fail while constructing the child process environment dictionary.

Fixes:

```powershell
[Environment]::GetEnvironmentVariables('Process').Keys | Where-Object { $_ -ieq 'path' }

$cleanPath = $env:Path
Remove-Item Env:Path -ErrorAction SilentlyContinue
Remove-Item Env:PATH -ErrorAction SilentlyContinue
Set-Item Env:Path $cleanPath
```

If it persists, close and reopen the terminal / Codex session, then check Windows user and system environment variables and keep only one `Path` entry.

### Vite Dev Server Does Not Stay Reachable

In managed Codex shell commands, long-running foreground commands can be killed when the command times out. Background launch attempts may also fail because of the `Path` / `PATH` issue or because the managed shell cleans up child processes.

For normal local development, run Vite from a regular user terminal:

```powershell
cd D:\UserData\Documents\Luminara\frontend
npm.cmd run dev -- --host 127.0.0.1 --port 5173
```

Then open:

```text
http://127.0.0.1:5173
```

If the port is busy, use another port:

```powershell
npm.cmd run dev -- --host 127.0.0.1 --port 5174
```

For Codex verification, prefer a production build when a persistent dev server is not required:

```powershell
cd frontend
npm.cmd run build
```

### Background Jobs / Child Processes Disappear

Codex `shell_command` runs in a short-lived managed PowerShell context. `Start-Job`, `Start-Process`, `python -m http.server`, and `npm.cmd run dev` may not survive after the command ends, times out, or the shell session is recycled. Jobs created in one shell command may also be invisible to the next command.

Recommended approach:

- Use a normal user terminal for persistent dev servers.
- Use `npm.cmd run build` for deterministic frontend verification.
- Use dedicated browser / preview tooling when visual verification through Codex is required.
- Do not treat failure to keep a background server alive in Codex as evidence that the Vue or Django app is broken.

## Common Commands

Run Django checks:

```powershell
python manage.py check
```

Run migrations:

```powershell
python manage.py migrate
```

Start Django development server:

```powershell
python manage.py runserver 127.0.0.1:8000
```

Install Python dependencies:

```powershell
python -m pip install -r requirements.txt
```

Install frontend dependencies:

```powershell
cd frontend
npm.cmd install
```

Build Vue frontend for Django:

```powershell
cd frontend
npm.cmd run build
```

Run Vue development server:

```powershell
cd frontend
npm.cmd run dev
```

## Current Routing

- `http://127.0.0.1:8000/`: Vue frontend served from `static/frontend/index.html`.
- `http://127.0.0.1:8000/admin/`: Django admin with simple-ui.
- Any non-admin path is currently treated as a Vue SPA path.

## Important Configuration Notes

- `simpleui` must stay before `django.contrib.admin` in `INSTALLED_APPS`.
- `LANGUAGE_CODE` is set to `zh-hans`.
- `STATICFILES_DIRS` includes `BASE_DIR / 'static'`.
- `mimetypes.add_type('application/javascript', '.js', True)` is used so Django serves Vite-built JS correctly on Windows.
- Vite uses `base: '/static/frontend/'` and outputs to `../static/frontend`.

## Development Rules

- After editing Vue files, run `npm.cmd run build` before verifying through Django.
- Keep `frontend/node_modules/`, `.venv/`, `db.sqlite3`, logs, and Python caches out of Git.
- Do not remove Django admin routes when changing frontend routing.
- Prefer adding future API routes under a clear prefix such as `/api/` so they do not conflict with Vue SPA fallback routes.
- Run `python manage.py check` after changing Django settings, URLs, models, or views.

## Admin

A Django superuser exists for local development. Avoid committing secrets or plain-text credentials into project files.
