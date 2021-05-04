.PHONY: requirements.txt format-code makemessages test

requirements.txt:
	pip-compile --generate-hashes --output-file=requirements.txt requirements.in

format-code:
	black .

test:
	/app/docker/run-tests.sh

messages:
	python /app/manage.py makemessages -a --no-location --no-obsolete
