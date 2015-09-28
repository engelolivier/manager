from rest_framework import viewsets, serializers
from .models import *


class EmployeeSerializer(serializers.HyperlinkedModelSerializer):
    
    class Meta:
        model = Employee
        fields = ('id', 'firstname', 'lastname' )

class SprintSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Sprint
        fields = ('id', 'name', 'date_start', 'date_end', )

class TaskSerializer(serializers.HyperlinkedModelSerializer):
    
    employees = EmployeeSerializer(many=True, read_only=True)
    sprint    = SprintSerializer(read_only=True)

    class Meta:
        model = Task
        fields = ('id', 'name', 'date_start', 'date_end', 'priority', 'employees', 'sprint', 'status'  )

    def create(self, validated_data):

        instance = Task.objects.create(**validated_data)
        instance = self.relations(instance)
        instance.save()
        return instance

    def update(self, instance, validated_data):

        instance = self.relations(instance)
        instance.__dict__.update(**validated_data)
        instance.save()
        return instance

    def relations(self, instance):

        try:
            sprint = int( self.initial_data['sprint']['id'] )
            instance.sprint = Sprint.objects.get(pk=sprint)
        except:
            pass

        try:
            employees_id_request = [int(employee['id']) for employee in self.initial_data['employees'] ]
            employees_id_base    = [x.id for x in instance.employees.all()] 

            # delete
            for employee_id in set(employees_id_base).difference(employees_id_request): 
                instance.employees.remove( Employee.objects.get(pk=employee_id) )

            # add
            for employee_id in set(employees_id_request).difference(employees_id_base):
                instance.employees.add( Employee.objects.get(pk=employee_id) )
        except:
            pass

        return instance