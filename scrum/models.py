#!/usr/bin/env python
# coding: utf-8

from django.db import models
from django.contrib.auth.models import User
from manager import settings

class Employee(models.Model):

	firstname     = models.CharField(max_length=100)
	lastname      = models.CharField(max_length=100)
	user          = models.OneToOneField(User, related_name="employee", null=True, blank=True)

	class Meta:
		verbose_name = "employee"
		verbose_name_plural = "employees"
	
	def __str__(self):
		return "{} {}".format(self.firstname, self.lastname, )

class Sprint(models.Model):

	name          = models.CharField(max_length=100)
	progression   = models.PositiveIntegerField(null=True, blank=True, default=0)
	description   = models.CharField(max_length=100)
	date_creation = models.DateTimeField(auto_now_add=True)
	date_start    = models.DateField(auto_now_add=False, null=True, blank=True)
	date_end      = models.DateField(auto_now_add=False, null=True, blank=True)

	class Meta:
		verbose_name = "sprint"
		verbose_name_plural = "sprint"
		ordering = ['-id']
	
	def __str__(self):
		return "{}".format(self.name, )

class Task(models.Model):

	name          = models.CharField(max_length=100)
	status        = models.PositiveIntegerField(choices=settings.TASK_STATUS, default=0)
	progression   = models.PositiveIntegerField(null=True, blank=True, default=0)
	description   = models.CharField(max_length=100)
	date_creation = models.DateTimeField(auto_now_add=True)
	date_start    = models.DateTimeField(auto_now_add=False, null=True, blank=True)
	date_end      = models.DateTimeField(auto_now_add=False, null=True, blank=True)
	employees     = models.ManyToManyField('Employee', blank=True, related_name="tasks")
	creator       = models.ForeignKey(Employee, null=True, blank=True)
	priority      = models.PositiveIntegerField(null=True, blank=True)
	sprint        = models.ForeignKey('Sprint', null=True, blank=True)

	class Meta:
		verbose_name = "task"
		verbose_name_plural = "tasks"
		ordering = ['priority']
	
	def __str__(self):
		return "{}".format(self.name, )


