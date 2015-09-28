# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('erp', '0002_auto_20150926_1907'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='productitem',
            name='attribute',
        ),
        migrations.AddField(
            model_name='productitem',
            name='attribute',
            field=models.ManyToManyField(to='erp.Attribute'),
        ),
    ]
