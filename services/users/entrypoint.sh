#!/bin/sh

echo "Waiting for postgres.."

#create users db with port 5432
while ! nc -z users-db 5432; do
	sleep 0.1
done

echo "PostgreSQL started"

python3 manage.py run -h 0.0.0.0
