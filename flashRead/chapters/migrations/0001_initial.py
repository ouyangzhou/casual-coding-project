# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Chapter',
            fields=[
                ('chid', models.AutoField(primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=50)),
                ('file_location', models.CharField(max_length=255)),
                ('chapter_number', models.IntegerField()),
                ('wordcount', models.IntegerField()),
                ('date_updated', models.DateTimeField(verbose_name='date added')),
                ('book', models.ForeignKey(to='books.Book')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
