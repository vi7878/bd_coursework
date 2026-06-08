#!/bin/sh


echo "Waiting for postgres..."
while ! nc -z db 5432; do
  sleep 0.1
done
echo "PostgreSQL started"

python manage.py makemigrations core monitoring public
python manage.py migrate
python manage.py collectstatic --no-input


echo "from core.models import User; User.objects.filter(username='admin').exists() or User.objects.create_superuser('admin', 'admin@example.com', 'adminpass', role='admin')" | python manage.py shell


python manage.py populate_data

exec "$@"
