#!/bin/bash


echo "BUILD START"

# Ensure pip is installed
python3.9 -m ensurepip --default-pip
python3.9 -m pip install --upgrade pip setuptools wheel

# Install Django and dependencies
python3.9 -m pip install -r requirements.txt

# Create the output directory for static files
mkdir -p staticfiles_build

# Run Django collectstatic and move files to `staticfiles_build`
python3.9 manage.py collectstatic --noinput --clear
cp -r static/* staticfiles_build/  # Ensure files are inside `staticfiles_build`

# Apply database migrations
python3.9 manage.py migrate

echo "BUILD END"
