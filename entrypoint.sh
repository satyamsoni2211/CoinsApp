#!/bin/bash
python3 manage.py collectstatic --noinput
echo "$@"
exec "$@"