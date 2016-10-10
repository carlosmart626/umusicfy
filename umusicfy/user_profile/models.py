# encoding:utf-8
import time
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.conf import settings
from django.template.defaultfilters import slugify

from songs.models import Song, Artist

from .tasks import send_email_notification_task


def upload_to_profile(instance, filename):
    return 'user/%s/%s' % (instance.user.username, filename)


class UserProfile(models.Model):
    user = models.OneToOneField(User)
    profile_picture = models.ImageField(upload_to=upload_to_profile, blank=True, null=True)
    biography = models.TextField(blank=True, null=True)
    following = models.ManyToManyField(User, related_name='users_following', blank=True, null=True)
    artist_following = models.ManyToManyField(Artist, related_name='artist_following', blank=True, null=True)

    def get_user_playlist(self):
        return PlayList.objects.filter(owner=self.user)

    def get_followers(self):
        return UserProfile.objects.filter(following=self.user)

    def get_playlists_following(self):
        return PlayList.objects.filter(followers=self.user)

    class Meta:
        verbose_name = _('User Profile')
        verbose_name_plural = _('Users Profile')

    def __unicode__(self):
        return str(self.user)


class PlayList(models.Model):
    owner = models.ForeignKey(User)
    title = models.CharField(max_length=250)
    title_slug = models.SlugField(max_length=250, blank=True, null=True)
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
        self.title_slug = slugify(self.title)
        super(self.__class__, self).save(*args, **kwargs)

    def get_duration_time(self):
        duration = 0
        for song in self.songs.all():
            duration = duration + song.duration
        return time.strftime("%H:%M:%S", time.gmtime(duration))

    def get_songs_number(self):
        number_songs = 0
        for song in self.songs.all():
            number_songs += 1
        return number_songs

    def __unicode__(self):
        return str(self.title)


class SongsPlaylist(models.Model):
    playlist = models.ForeignKey(PlayList)
    song = models.ForeignKey(Song)
    order = models.IntegerField(default=0)
    added_time = models.DateField(auto_now_add=True)


def send_email_notification(sender, instance, created, **kwargs):
    send_email_notification_task(instance.owner, instance)

post_save.connect(send_email_notification, sender=PlayList)
