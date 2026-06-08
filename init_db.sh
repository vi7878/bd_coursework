#!/bin/bash
python manage.py makemigrations core monitoring public
python manage.py migrate
python manage.py collectstatic --no-input



echo "from core.models import User; User.objects.filter(username='admin').exists() or User.objects.create_superuser('admin', 'admin@example.com', 'adminpass', role='admin')" | python manage.py shell
