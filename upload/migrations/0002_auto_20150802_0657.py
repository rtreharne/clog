# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('upload', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cell',
            name='file',
            field=models.FileField(upload_to=b'cells', verbose_name='Cell'),
        ),
    ]
