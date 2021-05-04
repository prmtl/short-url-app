#!/bin/bash

postgres_ready () {
  dockerize -wait 'tcp://database:5432' -timeout 5s
}

until postgres_ready; do
  >&2 echo 'DB is unavailable - sleeping'
done

# It is also possible to wait for other services as well: redis, elastic, mongo
>&2 echo 'DB ready!'

py.test -vvv --black --isort --flake8

./docker/lint-messages.sh

# Check that all migrations worked fine:
python manage.py makemigrations --dry-run --check || (echo 'Error' && exit 1)
