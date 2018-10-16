#!/bin/sh
set -ex

export DJANGO_SETTINGS_MODULE=config.settings.test

pip install -r /code/requirements/test.txt
# Ensure there are no missing migrations
# python manage.py makemigrations --dry-run | grep 'No changes detected' || (echo 'There are changes which require migrations.' && exit 1)

# Run unittests and coverage report
coverage erase
coverage run manage.py test --noinput --keepdb --settings="$DJANGO_SETTINGS_MODULE" "$@"
#coverage html -d reports

# Check code style
#/venv/bin/flake8 .
