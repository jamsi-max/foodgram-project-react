#!/bin/sh

set -e

ls -la /vol/
ls -la /vol/web

whoami

python manage.py wait_for_db
python manage.py collectstatic --noinput
python manage.py makemigrations
python manage.py migrate
python manage.py addcsvdata

backend/uwsgi --socket :9000 --module backend.wsgi