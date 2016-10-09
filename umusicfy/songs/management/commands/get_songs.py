# -*- coding: utf-8 -*-
'''
Use the ``mockups`` command like this::

    django-admin.py mockups [options] app.Model:# [app.Model:# ...]

Its nearly self explanatory. Supply names of models, prefixed with their app
name. After that, place a colon and tell the command how many objects you want
to create. Here is an example of how to create three categories and twenty
entries for you blogging app::

    django-admin.py mockups blog.Category:3 blog.Entry:20

Voila! You have ready to use testing data populated to your database. The
model fields are filled with data by producing randomly generated values
depending on the type of the field. E.g. text fields are filled with lorem
ipsum dummies, date fields are populated with random dates from the last
years etc.

There are a few command line options available. Mainly to control the
behavior of related fields. If foreingkey or many to many fields should be
populated with existing data or if the related models are also generated on
the fly. Please have a look at the help page of the command for more
information::

    django-admin.py help mockups
'''
from django.core.management.base import BaseCommand
import json
from pprint import pprint
from django.conf import settings


class Command(BaseCommand):
    help = (
        u'Get songs.'
    )

    def handle(self, *attrs, **options):
        with open(settings.BASE_DIR + '/data.json') as data_file:
            data = json.load(data_file)
        pprint(data)
        dict(data)
        print (len(data['artists']))
