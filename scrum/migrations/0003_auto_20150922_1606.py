# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('scrum', '0002_auto_20150922_1431'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sprint',
            name='date_end',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='sprint',
            name='date_start',
            field=models.DateField(blank=True, null=True),
        ),
    ]
