#!/usr/bin/env python
# coding: utf-8

from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.http import *
from django.views.generic import TemplateView
from manager import settings
from scrum.viewset import TaskSerializer
from rest_framework.renderers import JSONRenderer

from scrum.models import *

class LoginView(TemplateView):

	template_name = 'login.html'

	def post(self, request, **kwargs):

		username = request.POST.get('username', False)
		password = request.POST.get('password', False)
		user = authenticate(username=username, password=password)
		
		if not request.user.is_authenticated():
			try:
				login(request, user)
			except:
				pass

		if request.user.is_authenticated():
			return self.render_index(request)

		return render(request, self.template_name)

	def get(self, request, **kwargs):

		if request.user.is_authenticated():
			return self.render_index(request)

		return render(request, self.template_name)


	def get_context_data(self, **kwargs):

		context = {}
		#context['employees'] = Employee.objects.all()
		context['TASK_STATUS'] = settings.TASK_STATUS
		return context


	def render_index(self, request):

		context = self.get_context_data()
		return render(request, "index.html", context)


class LogoutView(TemplateView):

	template_name = 'login.html'

	def get(self, request, **kwargs):

		logout(request)
		return render(request, self.template_name)

class DashBoardView(TemplateView):

	template_name = "dashboard.html"

	def get_context_data(self, **kwargs):

		context = {}
		context['tasks'] = Task.objects.all()
		return context

	def get(self, request, **kwargs):

		context = self.get_context_data()
		return render(request, self.template_name, context)

class BacklogView(TemplateView):

	template_name = "backlog.html"

	def get(self, request, **kwargs):

		context = {}
		context['sprints'] = Sprint.objects.all()
		return render(request, self.template_name, context)


class SprintView(TemplateView):

	template_name = "sprint.html"

	def get(self, request, **kwargs):

		context = {}
		context['employees'] = Employee.objects.all()
		last_sprint = Sprint.objects.all()[0]
		context['tasks'] = Task.objects.filter(sprint=last_sprint)

		return render(request, self.template_name, context)

class GetSprintTasksView(TemplateView):

	def post(self, request, **kwargs):

		sprint = int(kwargs['sprint'])
		sprint = Sprint.objects.get(pk=sprint)
		tasks = Task.objects.filter(sprint=sprint)
		
		data = []
		for task in tasks:
			data.append(TaskSerializer(task).data)
		
		return JsonResponse( data, safe=False )

class TaskChangePriorityView(TemplateView):

	def post(self, request, **kwargs):

		pk = kwargs['pk']
		positions = request.POST['positions']
		
		for i, pk in enumerate(positions.split(":")):
			Task.objects.filter(pk=pk).update(priority=i)

		return JsonResponse( { "ok" : 1} )

class TaskChangeStatus(TemplateView):

	def post(self, request, **kwargs):

		pk = int(kwargs['pk'])
		status = int(request.POST['status'])
		print(pk, status)
		Task.objects.filter(pk=pk).update(status=status)
		return JsonResponse( { "ok" : 1} )

class TasksActionView(TemplateView):

	def post(self, request, **kwargs):

		ids = [int(id) for id in request.POST['ids'].split(":")] 
		action = request.POST['action']
		tasks = Task.objects.filter(pk__in=ids)

		if action == "sprint":

			sprint = Sprint.objects.get(pk=int(request.POST['sprint']))
			tasks.update(sprint=sprint)

		elif action == "delete":

			tasks.delete()



		return JsonResponse( { "ok" : 1} )

# ------------------------------------------------------

