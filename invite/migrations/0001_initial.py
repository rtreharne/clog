# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Invitation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('email', models.EmailField(max_length=254)),
                ('key', models.CharField(max_length=8)),
                ('activated', models.BooleanField(default=False)),
                ('message', models.CharField(max_length=1000, blank=True)),
                ('owner', models.ForeignKey(to='profiles.UserProfile')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
