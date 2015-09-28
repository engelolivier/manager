#!/usr/bin/env python
# coding: utf-8

from django.contrib import admin

# Register your models here.


from scrum.models import *

# Register your models here.

# admin.site.register(User)
admin.site.register(Sprint)
admin.site.register(Employee)
admin.site.register(Task)