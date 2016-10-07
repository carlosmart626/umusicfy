# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-10-07 03:06
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import songs.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Album',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=250)),
                ('album_cover', models.ImageField(height_field=512, upload_to=songs.models.upload_to_artist, width_field=512)),
                ('publication_date', models.DateField()),
                ('rating', models.PositiveIntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Artist',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=250)),
                ('profile_picture', models.ImageField(height_field=512, upload_to=songs.models.upload_to_artist, width_field=512)),
                ('profile_hero_image', models.ImageField(height_field=300, upload_to=songs.models.upload_to_artist, width_field=1500)),
                ('followers', models.ManyToManyField(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Song',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=250)),
                ('rating', models.PositiveIntegerField(default=0)),
                ('duration', models.CharField(max_length=8)),
                ('album', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='songs.Album')),
            ],
        ),
    ]