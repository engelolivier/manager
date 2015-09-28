# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('scrum', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='sprint',
            options={'verbose_name': 'sprint', 'ordering': ['-id'], 'verbose_name_plural': 'sprint'},
        ),
        migrations.AddField(
            model_name='task',
            name='sprint',
            field=models.ForeignKey(to='scrum.Sprint', null=True),
        ),
    ]
