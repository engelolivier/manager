from rest_framework import viewsets, serializers
from .models import *
from .serializers import *


class AttributeViewSet(viewsets.ModelViewSet):

	queryset = Attribute.objects.all()
	serializer_class = AttributeSerializer

class AttributeGroupViewSet(viewsets.ModelViewSet):

	queryset = AttributeGroup.objects.all()
	serializer_class = AttributeGroupSerializer

class CustomerViewSet(viewsets.ModelViewSet):

	queryset = Customer.objects.all()
	serializer_class = CustomerSerializer

class EmployeeViewSet(viewsets.ModelViewSet):

	queryset = Employee.objects.all()
	serializer_class = EmployeeSerializer

class TicketViewSet(viewsets.ModelViewSet):

	queryset = Ticket.objects.all()
	serializer_class = TicketSerializer

class TicketItemViewSet(viewsets.ModelViewSet):

	queryset = TicketItem.objects.all()
	serializer_class = TicketItemSerializer

class ProductViewSet(viewsets.ModelViewSet):

	queryset = Product.objects.all()
	serializer_class = ProductSerializer

class ProductItemViewSet(viewsets.ModelViewSet):

	queryset = ProductItem.objects.all()
	serializer_class = ProductItemSerializer