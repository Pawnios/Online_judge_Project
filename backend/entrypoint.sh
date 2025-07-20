#!/bin/sh

# Wait for database to be ready
echo "Waiting for database..."
while ! pg_isready -h db -p 5432 -U pawni; do
  echo "Database is unavailable - sleeping"
  sleep 1
done
echo "Database is up - executing command"

# Run Django commands
python manage.py makemigrations
python manage.py migrate
python manage.py runserver 0.0.0.0:8000
