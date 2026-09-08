# Throttle Pitstop — Backend

Django + Django REST Framework API for the Throttle Pitstop store
(Anwar Center, Karen). Currently covers **Phase 0–2** of the build plan:
project foundations, auth, and the product catalog.

## Stack
- Django 5 + Django REST Framework
- PostgreSQL
- JWT auth (djangorestframework-simplejwt)
- django-admin-interface for a branded admin panel

## Quick start (local, without Docker)

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

cp .env.example .env
# edit .env: at minimum set a real DJANGO_SECRET_KEY and Postgres credentials.
# You need a local Postgres running with a matching DB/user, or use Docker
# instead (see below), which handles Postgres for you.

python manage.py migrate
python manage.py createsuperuser
python manage.py seed_catalog   # optional: adds sample products
python manage.py runserver
```

API is now at `http://localhost:8000/api/`, admin at `http://localhost:8000/admin/`.

## Quick start (Docker, recommended)

```bash
cp .env.example .env
# edit .env with real values
docker compose up --build
```

This starts Postgres + the Django app together. Then, in another terminal:

```bash
docker compose exec web python manage.py createsuperuser
docker compose exec web python manage.py seed_catalog
```

## Endpoints so far

| Method | Endpoint                  | Purpose                              |
|--------|----------------------------|---------------------------------------|
| GET    | `/api/health/`             | Confirms the API is up (frontend uses this) |
| POST   | `/api/auth/register/`      | Customer sign-up                     |
| POST   | `/api/auth/login/`         | Get JWT access/refresh tokens        |
| POST   | `/api/auth/refresh/`       | Refresh an access token              |
| GET    | `/api/auth/me/`            | Logged-in user's own profile         |
| GET    | `/api/categories/`         | List categories                      |
| GET    | `/api/products/`           | List active products (paginated, filter by `?category__slug=`) |
| GET    | `/api/products/<slug>/`    | Product detail                       |

## Managing products

Everything is managed from Django admin at `/admin/` — add categories,
products, and upload product photos there. No separate admin UI needed;
this is intentional (see the build plan's Phase 1 notes).

## What's not built yet

Cart, checkout, orders, and M-Pesa integration are Phase 3–5 of the
build plan — not in this drop. See `throttle-pitstop-build-plan.md`.

## Deploying

- Set `DJANGO_SETTINGS_MODULE=config.settings.prod`
- Set `DJANGO_DEBUG=False` and real `DJANGO_ALLOWED_HOSTS` in `.env`
- Put this behind Nginx with a real Postgres instance (a small VPS works fine at this scale)
