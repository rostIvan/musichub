#!/usr/bin/env bash

export APP_ENVIRONMENT=DOCKER

./manage.py collectstatic --noinput
./manage.py migrate --no-input

mkdir logs
touch ./logs/gunicorn.log ./logs/gunicorn-access.log
tail -n 0 -f ./logs/*.log &

RETRIES=5

until psql -h $PG_HOST -U $PG_USER -d $PG_DB -W $PG_PASSWORD -c "select 1" > /dev/null 2>&1 || [ $RETRIES -eq 0 ]; do
  echo "Waiting for postgres server, $((RETRIES--)) remaining attempts..."
  sleep 1
done

gunicorn --bind :8000 musichub.wsgi:application \
         --reload \
         --log-level=info \
         --log-file=./logs/gunicorn.log \
         --access-logfile=./logs/gunicorn-access.log

exec "$@"
