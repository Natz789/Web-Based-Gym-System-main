#!/bin/bash

# Exit on error
set -e

echo "========================================"
echo "Gym System - Post-Build Setup Script"
echo "========================================"

echo "Installing Python dependencies..."
pip install -r requirements.txt

echo "Collecting static files for production..."
python manage.py collectstatic --noinput

echo "Running database migrations..."
python manage.py migrate --noinput

echo "========================================"
echo "Build completed successfully!"
echo "========================================"
echo ""
echo "To create a superuser, run:"
echo "  python manage.py createsuperuser"
echo ""
echo "Or use the custom command:"
echo "  python manage.py createadmin"
