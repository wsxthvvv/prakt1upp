#!/bin/sh

while ! nc -z $DB_HOST_PGSQL $DB_PORT_PGSQL; do
  echo "Waiting for PostgreSQL..."
  sleep 1
done

echo "Start migration"
python manage.py migrate --noinput
echo "Migration compeled"

echo "start collecting staticfiles"
python manage.py collectstatic --noinput
echo "Collectings staticfiles completed"

echo "Start creating superuser"
python manage.py shell << END
from django.contrib.auth import get_user_model
import os

User = get_user_model()
username = os.getenv('DJANGO_SUPERUSER_USERNAME')
email = os.getenv('DJANGO_SUPERUSER_EMAIL')
password = os.getenv('DJANGO_SUPERUSER_PASSWORD')

if not User.objects.filter(username=username).exists():
    User.objects.create_superuser(username, email, password)
END

echo "Superuser created"

echo "Starting gunicorn"
exec gunicorn shop.wsgi:application \
    --bind 0.0.0.0:8000 \
    --workers 4 \
    --access-logfile - \
    --error-logfile -