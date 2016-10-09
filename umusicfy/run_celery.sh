#!/bin/sh
/usr/local/bin/celery --app=umusicfy.celery:app worker --loglevel=INFO
