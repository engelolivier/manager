#!/usr/bin/env python
# coding: utf-8

"""manager URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
	https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
	1. Add an import:  from my_app import views
	2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
	1. Add an import:  from other_app.views import Home
	2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
	1. Add an import:  from blog import urls as blog_urls
	2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""

from scrum.views import LoginView, LogoutView

from django.conf.urls import include, url
from django.contrib import admin


from rest_framework import routers
from scrum import views
from scrum import viewset
from erp import viewsets as viewsets_erp

router = routers.DefaultRouter()
router.register(r'task', viewset.TaskViewSet)
router.register(r'employee', viewset.EmployeeViewSet)
router.register(r'sprint', viewset.SprintViewSet)

router.register(r'attribute', viewsets_erp.AttributeViewSet)
router.register(r'attributegroup', viewsets_erp.AttributeGroupViewSet)
router.register(r'customer', viewsets_erp.CustomerViewSet)
router.register(r'employee', viewsets_erp.EmployeeViewSet)
router.register(r'ticket', viewsets_erp.TicketViewSet)
router.register(r'ticketitem', viewsets_erp.TicketItemViewSet)
router.register(r'product', viewsets_erp.ProductViewSet)
router.register(r'productitem', viewsets_erp.ProductItemViewSet)

urlpatterns = [
	url(r'^$', views.LoginView.as_view()),
	url(r'^docs/', include('rest_framework_swagger.urls')),
	url(r'^logout/$', views.LogoutView.as_view()),
	url(r'^api/', include(router.urls)),
	url(r'^task/change_priority/(?P<pk>\d+)', views.TaskChangePriorityView.as_view() ),
	url(r'^task/change_status/(?P<pk>\d+)', views.TaskChangeStatus.as_view() ),
	url(r'^task/actions/', views.TasksActionView.as_view() ),
	url(r'^sprint/tasks/(?P<sprint>\d+)', views.GetSprintTasksView.as_view() ),
	url(r'^dashboard/$', views.DashBoardView.as_view()),
	url(r'^backlog/$', views.BacklogView.as_view()),
	url(r'^sprint/$', views.SprintView.as_view()),
	url(r'^admin/', include(admin.site.urls)),
]
