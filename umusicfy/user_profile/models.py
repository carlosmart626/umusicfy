# encoding:utf-8

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.conf import settings

from songs.models import Song, Artist

from .tasks import send_email_notification_task


def upload_to_profile(instance, filename):
    return 'user/%s/%s' % (instance.username, filename)


class UserProfile(models.Model):
    user = models.OneToOneField(User)
    profile_picture = models.ImageField(upload_to=upload_to_profile, height_field=150, width_field=150)
    biography = models.TextField()
    following = models.ManyToManyField(User, related_name='users_following')
    artist_following = models.ManyToManyField(Artist, related_name='artist_following')

    class Meta:
        verbose_name = _('User Profile')
        verbose_name_plural = _('Users Profile')

    def __unicode__(self):
        return str(self.user.username)


class PlayList(models.Model):
    owner = models.ForeignKey(User)
    title = models.CharField(max_length=250)
    creation_time = models.DateField(auto_now_add=True)
    followers = models.ManyToManyField(User, related_name='playlist_followers')
    songs = models.ManyToManyField(Song, related_name='play_list_songs', through='SongsPlaylist')

    def save(self, *args, **kwargs):
        '''
        Send pushe notification
        '''
        if self.pk is not None:
            orig = PlayList.objects.get(pk=self.pk)
            if orig.songs.count() != self.songs.count():
                settings.pusher.trigger(str(self.title), u'update', {u'some': u'data'})
        super(self.__class__, self).save(*args, **kwargs)


class SongsPlaylist(models.Model):
    playlist = models.ForeignKey(PlayList)
    song = models.ForeignKey(Song)
    order = models.IntegerField(default=0)
    added_time = models.DateField(auto_now_add=True)


def send_email_notification(sender, instance, created, **kwargs):
    send_email_notification_task.delay()

post_save.connect(send_email_notification, sender=PlayList)
