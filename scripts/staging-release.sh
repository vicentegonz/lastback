#!/bin/sh

python manage.py flush --no-input &&
python manage.py migrate &&
python manage.py loaddata $(find | grep '^\.\/backend\/.*\/fixtures/.*' | rev | cut -d'/' -f1 | rev | tr '\n' ' ')
