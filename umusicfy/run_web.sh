#!/bin/sh
python manage.py migrate --settings=umusicfy.settings.prd
python manage.py collectstatic --settings=umusicfy.settings.prd
