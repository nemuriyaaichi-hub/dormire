#!/bin/bash
set -e

if [ -n "$1" ]; then
    exec "$@"
fi

python manage.py makemigrations
python manage.py migrate
python manage.py collectstatic --noinput

if [ "${ADMIN_AUTO_CREATE}" = "True" ]; then
    python manage.py custom_createsuperuser --noinput --email ${ADMIN_EMAIL} --password ${ADMIN_PASSWORD}
fi

export PGPASSWORD=${POSTGRES_PASSWORD} && psql -h ${POSTGRES_HOST} -U ${POSTGRES_USER} -d ${POSTGRES_DB} -f ./sql/init.sql

exec uwsgi --ini uwsgi.local.ini
