#!/bin/sh
set -e

until mysql -h $MYSQL_HOST -u $MYSQL_ROOT_USERNAME -p$MYSQL_ROOT_PASSWORD -e 'SELECT VERSION()'; do
  >&2 echo "MySQL is unavailable - sleeping"
  sleep 3
done

if [ "x$DJANGO_COLLECTSTATIC" = 'xon' ]; then
    echo "Collect static files"
    python3 manage.py collectstatic --noinput
fi

if [ "x$DJANGO_MIGRATE" = 'xon' ]; then
    echo "Apply database migrations"
    python3 manage.py migrate --noinput
fi


echo "Run local server"
python3 manage.py runserver 0.0.0.0:8000
