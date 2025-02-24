#!/bin/bash

echo "BUILD START"

# Install dependencies properly
pip install -r requirements.txt

# Run Django collectstatic
python manage.py collectstatic --noinput --clear

# Apply database migrations (if needed)
python manage.py migrate

echo "BUILD END"
