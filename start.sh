#!/bin/sh
# Container entrypoint (Render and docker compose). Free hosting tiers have
# no shell, so everything a fresh database needs happens here on boot.
set -e

python manage.py migrate --noinput
python manage.py collectstatic --noinput

# Admin login without a shell: set DJANGO_SUPERUSER_USERNAME,
# DJANGO_SUPERUSER_EMAIL and DJANGO_SUPERUSER_PASSWORD in the host's
# environment. Harmless once the user exists.
if [ -n "$DJANGO_SUPERUSER_USERNAME" ] && [ -n "$DJANGO_SUPERUSER_PASSWORD" ]; then
  python manage.py createsuperuser --noinput || echo "Superuser already exists, skipping."
fi

# Optional sample products (get_or_create, so safe to leave on).
if [ "$SEED_CATALOG" = "true" ]; then
  python manage.py seed_catalog
fi

exec gunicorn config.wsgi:application --bind "0.0.0.0:${PORT:-8000}" --workers 2 --timeout 60
