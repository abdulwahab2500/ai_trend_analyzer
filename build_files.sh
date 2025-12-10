#!/bin/bash

# Build script for Vercel deployment
# This script runs during the build phase on Vercel

echo "======================================"
echo "Starting Django build process..."
echo "======================================"

# Navigate to the Django project directory
cd ai_trend_analyzer

# Install Python dependencies
echo "Installing dependencies..."
pip install -r requirements.txt

# Collect static files (CSS, JS, images) into STATIC_ROOT
echo "Collecting static files..."
python manage.py collectstatic --noinput --clear

# Run database migrations (use with caution on serverless - see notes below)
echo "Running database migrations..."
python manage.py migrate --noinput

echo "======================================"
echo "Build completed successfully!"
echo "======================================"

# NOTE: For production deployments on Vercel with serverless functions:
# - SQLite is NOT recommended for production (data will be lost between deployments)
# - Consider using PostgreSQL, MySQL, or another managed database service
# - You may want to comment out the 'migrate' command above if using external DB
# - Migrations should be run manually or via CI/CD for production databases
