from __future__ import unicode_literals

from django.apps import AppConfig
from django.contrib import algoliasearch

from .index import SongIndex


class SongsConfig(AppConfig):
    name = 'songs'

    def ready(self):
        Song = self.get_model('Song')
        algoliasearch.register(Song, SongIndex)
