from __future__ import unicode_literals
from django.contrib.auth.models import User
from django.db import models


def upload_to_artist(instance, filename):
    return 'artits/%s/%s' % (instance.username, filename)


class Artist(models.Model):
    """
    Model Artist
    """
    name = models.CharField(max_length=250)
    profile_picture = models.ImageField(upload_to=upload_to_artist, height_field=512, width_field=512)
    profile_hero_image = models.ImageField(upload_to=upload_to_artist, height_field=300, width_field=1500)
    followers = models.ManyToManyField(User)

    def get_albums(self):
        return Album.objects.filter(artist=self)

    def get_songs(self):
        return Song.objects.filter(album__artist=self)


class Album(models.Model):
    """
    Model Album
    """
    name = models.CharField(max_length=250)
    album_cover = models.ImageField(upload_to=upload_to_artist, height_field=512, width_field=512)
    publication_date = models.DateField()
    rating = models.PositiveIntegerField(default=0)

    def get_songs(self):
        return Song.objects.filter(album=self)


class Song(models.Model):
    """
    Model Song
    """
    title = models.CharField(max_length=250)
    rating = models.PositiveIntegerField(default=0)
    album = models.ForeignKey(Album)
    duration = models.CharField(max_length=8)
