# short-url-app

This is the backend server application for X project.

## Configuration


### Commands

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
