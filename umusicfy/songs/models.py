from __future__ import unicode_literals
import time
from django.contrib.auth.models import User
from django.db import models
from django.template.defaultfilters import slugify
from django.utils.encoding import smart_unicode


def upload_to_artist(instance, filename):
    return 'artits/%s/%s' % (instance.username, filename)


class Artist(models.Model):
    """
    Model Artist
    """
    name = models.CharField(max_length=50)
    name_slug = models.SlugField(max_length=50, blank=True, null=True)
    profile_picture = models.ImageField(upload_to=upload_to_artist, height_field=512, width_field=512)
    profile_hero_image = models.ImageField(upload_to=upload_to_artist, height_field=300, width_field=1500)
    followers = models.ManyToManyField(User)

    def save(self, *args, **kwargs):
        '''
        Override to update slug field at product after define name
        '''
        self.name_slug = slugify(self.name)
        super(self.__class__, self).save(*args, **kwargs)

    def get_albums(self):
        return Album.objects.filter(artist=self)

    def get_songs(self):
        return Song.objects.filter(album__artist=self)

    def __unicode__(self):
        return smart_unicode(self.name)


class Album(models.Model):
    """
    Model Album
    """
    name = models.CharField(max_length=50)
    name_slug = models.SlugField(max_length=50, blank=True, null=True)
    album_cover = models.ImageField(upload_to=upload_to_artist, height_field=512, width_field=512)
    artist = models.ForeignKey(Artist, blank=True, null=True)
    publication_date = models.DateField()
    rating = models.PositiveIntegerField(default=0)

    def save(self, *args, **kwargs):
        '''
        Override to update slug field at product after define name
        '''
        self.name_slug = slugify(self.name)
        super(self.__class__, self).save(*args, **kwargs)

    def get_songs(self):
        return Song.objects.filter(album=self)

    def __unicode__(self):
        return "%s's %s" % (smart_unicode(self.artist), smart_unicode(self.name))


class Song(models.Model):
    """
    Model Song
    """
    title = models.CharField(max_length=50)
    rating = models.PositiveIntegerField(default=0)
    album = models.ForeignKey(Album)
    duration = models.IntegerField(default=0)

    def get_duration_time(self):
        return time.strftime("%M:%S", time.gmtime(self.duration))

    def __unicode__(self):
        return smart_unicode(self.title)
