#!/bin/sh
#python /code/manage.py collectstatic --noinput
#/usr/local/bin/gunicorn config.wsgi -w 4 -b 0.0.0.0:5000 --chdir=/code
service ssh start
honcho start
