#!/bin/sh
set -e

#touch /home/LogFiles/node_${WEBSITE_ROLE_INSTANCE_ID}_out.log
#echo "$(date) Container started" >> /home/LogFiles/node_${WEBSITE_ROLE_INSTANCE_ID}_out.log

#until psql $DATABASE_URL -c '\l'; do
#  >&2 echo "Postgres is unavailable - sleeping"
#  sleep 1
#done
#
#>&2 echo "Postgres is up - continuing"

if [ "x$DJANGO_MIGRATE" = 'xon' ]; then
    python manage.py migrate --noinput
fi

if [ "x$DJANGO_COLLECTSTATIC" = 'xon' ]; then
    python manage.py collectstatic --noinput
fi

exec "$@"
