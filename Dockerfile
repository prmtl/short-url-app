FROM python:3.9.1-slim

ARG GIT_COMMIT=unspecified

ENV GIT_COMMIT=$GIT_COMMIT \
  # python
  PYTHONFAULTHANDLER=1 \
  PYTHONUNBUFFERED=1 \
  PYTHONHASHSEED=random \
  # pip
  PIP_NO_CACHE_DIR=off \
  PIP_DISABLE_PIP_VERSION_CHECK=on \
  PIP_DEFAULT_TIMEOUT=100 \
  # config
  SECRET_KEY=C8\zj)6(*euAF@~HU}w36SVC%.&^n]-s:Hy+dP*N_JRn#N-%R!3W)\2h@/jpkQgr1 \
  DEBUG=False \
  ADDITIONAL_ALLOWED_HOSTS= \
  SENTRY_DSN="" \
  ENV=develop \
  DATABASE_URL=postgres://postgres:postgres@database/shorturl \
  DATABASE_CHECK_ENDPOINT=tcp://database:5432 \
  DOMAIN_NAME=localhost \
  DOCKERIZE_VERSION=v0.6.1

RUN apt-get update && \
    apt-get install -y \
    # psycopg2 dependencies
    gcc libpq-dev python3-dev \
    # Translations dependencies
    gettext \
    # utilities
    make wget tar \
  && apt-get clean \
  && rm -rf /var/lib/apt/lists/* \
  && pip install pip-tools==5.4.0

RUN wget https://github.com/jwilder/dockerize/releases/download/$DOCKERIZE_VERSION/dockerize-linux-amd64-$DOCKERIZE_VERSION.tar.gz \
    && tar -C /usr/local/bin/ -xzvf dockerize-linux-amd64-$DOCKERIZE_VERSION.tar.gz \
    && rm dockerize-linux-amd64-$DOCKERIZE_VERSION.tar.gz

WORKDIR /app

COPY requirements.txt /app
RUN pip-sync requirements.txt

COPY . /app

CMD ["/app/docker/run.sh"]
