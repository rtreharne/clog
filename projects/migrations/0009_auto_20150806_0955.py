# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0008_auto_20150805_1414'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='start_date',
            field=models.DateTimeField(default=datetime.datetime(2015, 8, 6, 9, 55, 5, 303800)),
        ),
        migrations.AlterField(
            model_name='project',
            name='updated',
            field=models.DateTimeField(default=datetime.datetime(2015, 8, 6, 9, 55, 5, 303832)),
        ),
    ]
