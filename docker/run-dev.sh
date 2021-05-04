#!/usr/bin/env sh

set -x
set -o errexit
set -o nounset

python /app/manage.py migrate --noinput
python /app/manage.py collectstatic --noinput
python /app/manage.py compilemessages

python /app/manage.py runserver "0.0.0.0:5000" -v 3
