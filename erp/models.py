from django.db import models


class AttributeGroup(models.Model):

	name       = models.CharField(max_length=100)

	def __str__(self):
		return "{}".format(self.name, )

class Attribute(models.Model):

	value            = models.CharField(max_length=100)
	attribute_group  = models.ForeignKey('AttributeGroup', null=True, blank=True, related_name="attributes")
	
	def __str__(self):
		return "{}".format(self.value, )

class Customer(models.Model):

	firstname     = models.CharField(max_length=100)
	lastname      = models.CharField(max_length=100)

	def __str__(self):
		return "{} {}".format(self.firstname, self.lastname, )

class Employee(models.Model):

	firstname     = models.CharField(max_length=100)
	lastname      = models.CharField(max_length=100)

	def __str__(self):
		return "{} {}".format(self.firstname, self.lastname, )

class Ticket(models.Model):

	customer     = models.ForeignKey('Customer')
	employee     = models.ForeignKey('Employee')
	
	def __str__(self):
		return "{}".format(self.name, )

class TicketItem(models.Model):

	ticket     = models.ForeignKey('Ticket')
	product    = models.ForeignKey('Product', null=True, blank=True)
	name       = models.CharField(max_length=100)
	price_ttc = models.FloatField()
	
	def __str__(self):
		return "{} {}".format(self.id, self.name )

class Product(models.Model):

	name      = models.CharField(max_length=255)
	price_ttc = models.FloatField()
	
	def __str__(self):
		return "{}".format(self.name, )

class ProductItem(models.Model):

	product    = models.ForeignKey('Product')
	attribute  = models.ManyToManyField('Attribute')
	ean13      = models.CharField(max_length=14, null=True, blank=True)
	
	def __str__(self):
		return "{} {} {}".format(self.product, self.attribute, self.ean13 )



