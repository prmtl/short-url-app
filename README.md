# short-url-app

This is the backend server application for X project.

The stack consists of Django with GraphQL API wrapped in Docker container. It uses "boilerplate" of my creation
to speed up dev process and save time on things like project and dev env setup.

## Running

Project is wrapped in Docker container and this is how it is intended to run. A docker-compose
file is added that allows to run whole stach (app + DB):

	docker-compose up -d

It is also usefull to create superuser to access Django Admin Panel:

	docker-compose run --rm backend /bin/bash -c 'python /app/manage.py createsuperuser'


Tests can be run with:

	docker-compose run --rm backend /app/docker/run-tests.sh


## URLs

http://localhost:5000/graphql/ - GraphQL endpoint & GraphQL Playground
http://localhost:5000/backend/admin/ - Django Admin Panel


## Commands

Commands to run inside running container.

Compile `requirements.txt` file (need to have `pip-tools` package installed locally):

	make requirements.txt

Format code:

	make format-code

Run tests and linters:

	make test

Update translations:

  make messages

Update translations (inside container):

  python ./manage.py makemessages -a --no-location --no-obsolete

Including loction of translation strings forces recreation of new translation
file when we just add a new line in file above some translations - line numbers
are changing, so we skip it. Also unused strings are removed.
