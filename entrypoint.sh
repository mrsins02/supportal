#!/bin/sh

run_migrations() {
    echo "Waiting for database to be ready..."
    until python manage.py migrate; do
        echo "Database not ready yet. Retrying in 5 seconds..."
        sleep 5
    done
    echo "Migrations applied successfully."
}

run_migrations

exec "$@"