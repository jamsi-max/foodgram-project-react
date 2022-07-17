#!/bin/sh

set -e

ls -la /vol/
ls -la /vol/web

whoami

backend/python manage.py wait_for_db
backend/python manage.py collectstatic --noinput
backend/python manage.py makemigrations
backend/python manage.py migrate
backend/python manage.py addcsvdata

backend/uwsgi --socket :9000 --module backend.wsgi