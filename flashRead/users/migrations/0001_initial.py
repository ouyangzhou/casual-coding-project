# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('chapters', '0001_initial'),
        ('books', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID', auto_created=True)),
                ('about', models.CharField(max_length=255)),
                ('gender', models.CharField(max_length=140, choices=[('Male', 'Male'), ('Female', 'Female'), ("It's a secret. Shh..", "It's a secret. Shh.."), ('Others', 'Others')])),
                ('vote_of_day', models.IntegerField(default=0)),
                ('vote_time', models.DateTimeField(default=datetime.datetime(2014, 11, 28, 2, 3, 23, 376327))),
                ('bookmark', models.ManyToManyField(related_name='bookmark', default='', to='chapters.Chapter')),
                ('favorites', models.ManyToManyField(related_name='favorited_by', default='', to='books.Book')),
                ('myuser', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
