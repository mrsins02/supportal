#!/bin/sh
set -e

# waiting to database ready
echo "Waiting for Postgresql to be ready..."
/usr/local/bin/wait-for-it.sh ${POSTGRES_HOST}:${POSTGRES_PORT} --timeout=60 --strict -- echo "Postgresql is up!"
echo "Running migrations..."
python3 manage.py migrate

# run server
python3 -m gunicorn --bind 0.0.0.0:8000 config.wsgi:application --reload --workers 3 --timeout 120
