from rest_framework import viewsets, serializers
from .models import *



class ModelSerializerCustom(serializers.ModelSerializer):

	def manytomany(self, instance, field_name, model):

		field = eval( 'instance.{}'.format(field_name) )
		
		ids_request = [x for x in self.initial_data[field_name].split(":") ]
		ids_base    = [x.id for x in field.all()] 

		# delete
		for pk in set(ids_base).difference(ids_request): 
			field.remove( model.objects.get(pk=pk) )

		# add
		for pk in set(ids_request).difference(ids_base):
			field.add( model.objects.get(pk=pk) )

		return instance


class AttributeSerializer(ModelSerializerCustom):
	
	class Meta:
		model = Attribute

class AttributeGroupSerializer(ModelSerializerCustom):
	
	class Meta:
		model = AttributeGroup

class CustomerSerializer(ModelSerializerCustom):
	
	class Meta:
		model = Customer

class EmployeeSerializer(ModelSerializerCustom):
	
	class Meta:
		model = Employee

class TicketSerializer(ModelSerializerCustom):
	
	class Meta:
		model = Ticket

class TicketItemSerializer(ModelSerializerCustom):
	
	class Meta:
		model = TicketItem

class ProductSerializer(ModelSerializerCustom):
	
	class Meta:
		model = Product

class ProductItemSerializer(ModelSerializerCustom):
	
	attribute = AttributeSerializer(many=True, read_only=False)

	def create(self, validated_data):

		del validated_data['attribute']
		instance = ProductItem.objects.create(**validated_data)
		instance = self.manytomany(instance, 'attribute', Attribute)
		return instance

	def update(self, instance, validated_data):

		instance = self.manytomany(instance, 'attribute', Attribute)
		instance.__dict__.update(**validated_data)
		instance.save()
		return instance

	class Meta:
		model = ProductItem
