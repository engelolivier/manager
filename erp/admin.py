#!/usr/bin/env python
# coding: utf-8

from django.contrib import admin

# Register your models here.


from .models import *

# Register your models here.

# admin.site.register(User)
admin.site.register(Attribute)
admin.site.register(AttributeGroup)
admin.site.register(Customer)
admin.site.register(Employee)
admin.site.register(Ticket)
admin.site.register(TicketItem)
admin.site.register(Product)
admin.site.register(ProductItem)