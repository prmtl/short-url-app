#!/bin/bash

set -o errexit
set -o nounset

echo "Linting translations..."

LANG=en
PO_FILE=locale/$LANG/LC_MESSAGES/django.po

# timestamps are recreated every time, so we get rid of them for diffing
ORIGINAL=`sed '/POT-Creation-Date/d' $PO_FILE`

#hack to keep the same inode for the file, so texteditors will not
# notiify about file modification
mv $PO_FILE "${PO_FILE}_orig"
cp "${PO_FILE}_orig" $PO_FILE

# regenerate messages and prepare new file for diffing
python ./manage.py makemessages -v 0 -a --no-location --no-obsolete
REGENERATED=`sed '/POT-Creation-Date/d' $PO_FILE`

# bring back original file
mv "${PO_FILE}_orig" $PO_FILE

diff <( echo "$ORIGINAL" ) <( echo "$REGENERATED" ) || (echo 'Error' && exit 1)

echo 'Translations OK'
