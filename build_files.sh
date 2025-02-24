#!/bin/bash

echo "BUILD START"

# Install dependencies correctly
python3.9 -m pip install -r requirements.txt

# Run Django collectstatic
python3.9 manage.py collectstatic --noinput --clear

# Apply migrations (if your project needs a database)
python3.9 manage.py migrate

# Create the correct build directory
mkdir -p staticfiles_build
cp -r static/* staticfiles_build/

echo "BUILD END"
