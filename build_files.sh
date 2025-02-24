#!/bin/bash

echo "BUILD START"

# Ensure Python and pip are installed
python3.9 -m ensurepip --default-pip
python3.9 -m pip install --upgrade pip setuptools wheel

# Install project dependencies
python3.9 -m pip install -r requirements.txt

# Run Django collectstatic
python3.9 manage.py collectstatic --noinput --clear

# Apply database migrations
python3.9 manage.py migrate

echo "BUILD END"
