# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0004_auto_20150802_0657'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='start_date',
            field=models.DateTimeField(default=datetime.datetime(2015, 8, 5, 12, 43, 3, 439722)),
        ),
        migrations.AlterField(
            model_name='project',
            name='updated',
            field=models.DateTimeField(default=datetime.datetime(2015, 8, 5, 12, 43, 3, 439753)),
        ),
    ]
