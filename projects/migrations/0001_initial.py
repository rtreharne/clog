# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=50)),
                ('description', models.TextField(max_length=200)),
                ('start_date', models.DateTimeField(default=datetime.datetime(2015, 8, 2, 6, 54, 24, 796331))),
                ('updated', models.DateTimeField(default=datetime.datetime(2015, 8, 2, 6, 54, 24, 796365))),
                ('owner', models.ForeignKey(to='profiles.UserProfile')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
