#!/bin/sh
#python /code/manage.py collectstatic --noinput
#/usr/local/bin/gunicorn config.wsgi -w 4 -b 0.0.0.0:8080 --chdir=/code

#!/bin/sh
python manage.py migrate
python manage.py runserver_plus 0.0.0.0:8000
