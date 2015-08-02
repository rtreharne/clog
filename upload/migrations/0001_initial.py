# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from decimal import Decimal


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Cell',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('notes', models.TextField(max_length=500)),
                ('file', models.FileField(upload_to=b'attachments', verbose_name='Attachment')),
                ('jsc', models.DecimalField(default=Decimal('0'), max_digits=6, decimal_places=3)),
                ('voc', models.DecimalField(default=Decimal('0'), max_digits=6, decimal_places=3)),
                ('ff', models.DecimalField(default=Decimal('0'), max_digits=6, decimal_places=3)),
                ('eff', models.DecimalField(default=Decimal('0'), max_digits=6, decimal_places=3)),
                ('date', models.DateTimeField(default=datetime.datetime.today)),
                ('label', models.CharField(max_length=128)),
                ('project', models.ForeignKey(verbose_name='Project', to='projects.Project')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
