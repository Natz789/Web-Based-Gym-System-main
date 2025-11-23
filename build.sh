#!/bin/bash

# Exit on error
set -e

echo "========================================"
echo "Starting Gym System Render Build"
echo "========================================"

# Update pip
echo "Updating pip..."
pip install --upgrade pip

# Install Python dependencies
echo "Installing Python dependencies..."
pip install -r requirements.txt

# Collect static files for production
echo "Collecting static files..."
python manage.py collectstatic --noinput

# Run database migrations
echo "Running database migrations..."
python manage.py migrate

# Create cache table for session management
echo "Creating cache table..."
python manage.py migrate --database=default

# Optional: Create superuser if using seed script
# Uncomment if you have a custom management command for creating admin
# echo "Creating superuser..."
# python manage.py createadmin

echo "========================================"
echo "Build completed successfully!"
echo "========================================"
