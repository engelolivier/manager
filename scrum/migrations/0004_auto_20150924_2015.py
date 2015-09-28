# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('scrum', '0003_auto_20150922_1606'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='status',
            field=models.PositiveIntegerField(choices=[(0, 'Todo'), (1, 'In Pogress'), (2, 'Finished')], default=0),
        ),
        migrations.AlterField(
            model_name='task',
            name='sprint',
            field=models.ForeignKey(to='scrum.Sprint', blank=True, null=True),
        ),
    ]
