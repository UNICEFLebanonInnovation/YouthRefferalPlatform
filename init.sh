#!/bin/bash
set -e

echo "Starting SSH ..."
service ssh start

#honcho start
#python /code/manage.py runserver 0.0.0.0:8080
/code/gunicorn config.wsgi -w 4 -b 0.0.0.0:8080 --chdir=/code
