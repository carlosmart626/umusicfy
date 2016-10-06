# encoding:utf-8

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User


class UserProfile(models.Model):
    user = models.OneToOneField(User)
    biography = models.TextField()
    friends = models.ManyToManyField(User)

    class Meta:
        verbose_name = _('User Profile')
        verbose_name_plural = _('Users Profile')

    def __unicode__(self):
        return str(self.user.username)
