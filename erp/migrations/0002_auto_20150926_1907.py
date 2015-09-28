# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('erp', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='productitem',
            name='ean13',
            field=models.CharField(blank=True, max_length=14, null=True),
        ),
        migrations.AlterField(
            model_name='attribute',
            name='attribute_group',
            field=models.ForeignKey(to='erp.AttributeGroup', blank=True, related_name='attributes', null=True),
        ),
    ]
