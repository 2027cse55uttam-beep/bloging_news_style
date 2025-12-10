#!/usr/bin/env bash
# Exit on error
set -o errexit

# 1. Packages Install
pip install -r requirements.txt

# 2. Static Files Collect (CSS/JS)
python manage.py collectstatic --no-input

# 3. Database Migration
python manage.py migrate