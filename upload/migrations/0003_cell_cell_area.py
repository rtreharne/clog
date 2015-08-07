# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from decimal import Decimal


class Migration(migrations.Migration):

    dependencies = [
        ('upload', '0002_auto_20150802_0657'),
    ]

    operations = [
        migrations.AddField(
            model_name='cell',
            name='cell_area',
            field=models.DecimalField(default=Decimal('0.25'), max_digits=6, decimal_places=3),
            preserve_default=True,
        ),
    ]
