#!/bin/sh

until nc -z $DB_HOST $DB_PORT; do
    sleep 1
done


cd src

python manage.py migrate


if [ "$DEBUG" = "True" ]; then
    python manage.py runserver 0.0.0.0:8000
else
    gunicorn settings.wsgi:application --bind 0.0.0.0:8000
fi
