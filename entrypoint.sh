#!/bin/bash

python3 manage.py collectstatic --noinput

set -e

until PGPASSWORD=$POSTGRES_PASSWORD psql -h "$PG_HOST" -U "$POSTGRES_USER" -c '\q'; do
  >&2 echo "Postgres is unavailable - sleeping"
  sleep 1
done

>&2 echo "Postgres is up - executing command"
exec "$@"
