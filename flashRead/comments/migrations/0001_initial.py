# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('chapters', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('coid', models.AutoField(primary_key=True, serialize=False)),
                ('content', models.CharField(max_length=255)),
                ('date_updated', models.DateTimeField(auto_now=True, auto_now_add=True)),
                ('chapter', models.ForeignKey(to='chapters.Chapter')),
                ('commentor', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
