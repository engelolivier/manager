# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Employee',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('firstname', models.CharField(max_length=100)),
                ('lastname', models.CharField(max_length=100)),
                ('user', models.OneToOneField(null=True, to=settings.AUTH_USER_MODEL, blank=True, related_name='employee')),
            ],
            options={
                'verbose_name': 'employee',
                'verbose_name_plural': 'employees',
            },
        ),
        migrations.CreateModel(
            name='Sprint',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100)),
                ('progression', models.PositiveIntegerField(blank=True, null=True, default=0)),
                ('description', models.CharField(max_length=100)),
                ('date_creation', models.DateTimeField(auto_now_add=True)),
                ('date_start', models.DateTimeField(blank=True, null=True)),
                ('date_end', models.DateTimeField(blank=True, null=True)),
            ],
            options={
                'ordering': ['-date_start'],
                'verbose_name': 'sprint',
                'verbose_name_plural': 'sprint',
            },
        ),
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100)),
                ('progression', models.PositiveIntegerField(blank=True, null=True, default=0)),
                ('description', models.CharField(max_length=100)),
                ('date_creation', models.DateTimeField(auto_now_add=True)),
                ('date_start', models.DateTimeField(blank=True, null=True)),
                ('date_end', models.DateTimeField(blank=True, null=True)),
                ('priority', models.PositiveIntegerField(blank=True, null=True)),
                ('creator', models.ForeignKey(to='scrum.Employee', blank=True, null=True)),
                ('employees', models.ManyToManyField(to='scrum.Employee', related_name='tasks', blank=True)),
            ],
            options={
                'ordering': ['priority'],
                'verbose_name': 'task',
                'verbose_name_plural': 'tasks',
            },
        ),
    ]
