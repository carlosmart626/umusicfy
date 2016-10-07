# encoding:utf-8

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User
from django.db.models.signals import post_save

from songs.models import Song


def upload_to_profile(instance, filename):
    return 'user/%s/%s' % (instance.username, filename)


class UserProfile(models.Model):
    user = models.OneToOneField(User)
    profile_picture = models.ImageField(upload_to=upload_to_profile, height_field=150, width_field=150)
    biography = models.TextField()
    friends = models.ManyToManyField(User)

    class Meta:
        verbose_name = _('User Profile')
        verbose_name_plural = _('Users Profile')

    def __unicode__(self):
        return str(self.user.username)


class PlayList(models.Model):
    owner = models.ForeingKey(User)
    creation_time = models.DateField(auto_now_add=True)
    followers = models.ManyToManyField(User)
    songs = models.ManyToManyField(Song, related_name='play_list_songs', through='SongsPlaylist')


class SongsPlaylist(models.Model):
    playlist = models.ForeignKey(PlayList)
    song = models.ForeignKey(Song)
    order = models.IntegerField(default=0)
    added_time = models.DateField(auto_now_add=True)


def send_email_notification(sender, instance, created, **kwargs):
    pass

post_save.connect(send_email_notification, sender=PlayList)
