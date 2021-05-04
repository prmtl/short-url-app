#!/usr/bin/env sh

set -x
set -o errexit
set -o nounset

# Need to be set to RDS in prod env
postgres_ready () {
  dockerize -wait $DATABASE_CHECK_ENDPOINT -timeout 5s
}

until postgres_ready; do
  >&2 echo 'DB is unavailable - sleeping'
done

# It is also possible to wait for other services as well: redis, elastic, mongo
>&2 echo 'DB ready!'

# We are using `gunicorn` for production, see:
# http://docs.gunicorn.org/en/stable/configure.html

# Run python specific scripts:
# Running migrations in startup script might not be the best option, see:
# docs/pages/template/production-checklist.rst
python /app/manage.py migrate --noinput
python /app/manage.py collectstatic --noinput
python /app/manage.py compilemessages

# Start gunicorn:
# Docs: http://docs.gunicorn.org/en/stable/settings.html
# Concerning `workers` setting see:
# https://github.com/wemake-services/wemake-django-template/issues/1022
/usr/local/bin/gunicorn server.wsgi \
  --reload \
  --workers=4 `# Sync worker settings` \
  --max-requests=2000 \
  --max-requests-jitter=400 \
  --bind="0.0.0.0:5000" \
  --chdir='/app'       `# Locations` \
  --log-file=- \
  --worker-tmp-dir='/dev/shm'
