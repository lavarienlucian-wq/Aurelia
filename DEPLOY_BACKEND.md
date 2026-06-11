# Backend Deployment

This Django backend is configured for a separate production deployment.

## Environment variables

Set these in the hosting provider:

- `DEBUG=False`
- `SECRET_KEY`: a long random secret
- `DATABASE_URL`: PostgreSQL connection string
- `ALLOWED_HOSTS`: backend host names, separated by commas
- `CSRF_TRUSTED_ORIGINS`: backend HTTPS origins, separated by commas
- `CORS_ALLOWED_ORIGINS`: frontend HTTPS origins, separated by commas
- `SECURE_SSL_REDIRECT`: set to `True` only if the hosting proxy does not already redirect HTTP to HTTPS
- `SECURE_HSTS_SECONDS`: set after confirming the backend is permanently HTTPS-only
- `SECURE_HSTS_PRELOAD`: keep `True` only when the backend domain should be eligible for HSTS preload
- `DJANGO_SUPERUSER_USERNAME`: admin username
- `DJANGO_SUPERUSER_EMAIL`: admin email
- `DJANGO_SUPERUSER_PASSWORD`: admin password

## Build commands

```powershell
pip install -r requirements.txt
python manage.py collectstatic --noinput
python manage.py migrate
python manage.py ensure_superuser --skip-if-missing
```

## Start command

```powershell
gunicorn luminara.wsgi:application
```

## Render blueprint

`render.yaml` creates a PostgreSQL database and a web service. Fill in the
private environment variables marked `sync: false` before the first deploy. If
you add the admin variables later, run this once from Render Shell:

```powershell
python manage.py ensure_superuser
```

The admin panel will be available at:

```text
https://<your-backend-host>/admin/
```
