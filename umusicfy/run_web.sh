#!/bin/sh
python manage.py migrate --settings=umusicfy.settings.prd
python manage.py collectstatic --no-input --settings=umusicfy.settings.prd
