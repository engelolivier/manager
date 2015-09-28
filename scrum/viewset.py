from rest_framework import viewsets, serializers
from scrum.models import *
from .serializers import *

class EmployeeViewSet(viewsets.ModelViewSet):

    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer

class SprintViewSet(viewsets.ModelViewSet):

    queryset = Sprint.objects.all()
    serializer_class = SprintSerializer

class TaskViewSet(viewsets.ModelViewSet):

    queryset = Task.objects.all()
    serializer_class = TaskSerializer





