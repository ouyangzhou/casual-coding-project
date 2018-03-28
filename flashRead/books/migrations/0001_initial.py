# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Book',
            fields=[
                ('bid', models.AutoField(primary_key=True, serialize=False)),
                ('title', models.CharField(default='', max_length=50)),
                ('genre', models.CharField(default='', max_length=50)),
                ('category', models.CharField(default='', max_length=100)),
                ('abstract', models.CharField(default='', max_length=255)),
                ('warning', models.BooleanField(default=True)),
                ('wordcount', models.IntegerField(default=0)),
                ('hits', models.IntegerField(default=0)),
                ('votes', models.IntegerField(default=0)),
                ('date_updated', models.DateTimeField(default='2011-01-01', verbose_name='date published')),
                ('status', models.CharField(default='', max_length=50)),
                ('author', models.ForeignKey(default=1, to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
