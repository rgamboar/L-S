from __future__ import unicode_literals

from django.db import models

# Create your models here.


class Warehouse(models.Model):
	name = models.CharField(max_length=150, null=False, unique=True)
	phone = models.CharField(max_length=150, null=False)
	rep = models.CharField(max_length=150, null=False)

	createDate = models.DateTimeField(auto_now=True)
	lastDate = models.DateTimeField(auto_now_add=True)

	def __unicode__(self):
		return self.name

class Driver(models.Model):
	name = models.CharField(max_length=150, null=False)
	phone = models.CharField(max_length=150, null=False)

	createDate = models.DateTimeField(auto_now=True)
	lastDate = models.DateTimeField(auto_now_add=True)

	def __unicode__(self):
		return self.name

class Truck(models.Model):
	plate = models.CharField(max_length=150, null=False, unique=True)
	is_rent = models.BooleanField(null=False)

	createDate = models.DateTimeField(auto_now=True)
	lastDate = models.DateTimeField(auto_now_add=True)

	def __unicode__(self):
		return self.plate


class Customer(models.Model):
	name = models.CharField(max_length=150, null=False)
	rut = models.CharField(max_length=150, null=False, unique=True)
	address = models.CharField(max_length=150, null=False)
	phone = models.CharField(max_length=150, null=False)

	rep = models.CharField(max_length=150, null=False)
	repAddress = models.CharField(max_length=150, null=False)
	repEmail = models.CharField(max_length=150, null=False)
	repPhone = models.CharField(max_length=150, null=False)
	pay = models.CharField(max_length=150, null=False)

	createDate = models.DateTimeField(auto_now=True)
	lastDate = models.DateTimeField(auto_now_add=True)

	def __unicode__(self):
		return self.name

class Freight(models.Model):
	authorName= models.CharField(max_length=300, null=False)
	createDate = models.DateTimeField(auto_now=True)
	sendDate = models.DateTimeField(null=True)
	lastDate = models.DateTimeField(auto_now_add=True)

	is_waiting=models.BooleanField(default=True)
	is_traveling = models.BooleanField(default=False)

	start = models.ForeignKey(Warehouse, null=False, related_name='travelStart')
	finish = models.ForeignKey(Warehouse, null=False, related_name='travelFinish')
	truck = models.ForeignKey(Truck, null=True)
	driver = models.ForeignKey(Driver, null=True)

	def __unicode__(self):
		return unicode(self.id)



class Package(models.Model):
	name = models.CharField(max_length=300, null=True)
	authorName= models.CharField(max_length=300, null=False)
	address= models.CharField(max_length=300, null=True)
	createDate = models.DateTimeField(auto_now=True)
	sendDate = models.DateTimeField(null=True)
	lastDate = models.DateTimeField(auto_now_add=True)

	is_waiting =models.BooleanField(default=True)
	risk = models.CharField(max_length=100, null=True)
	volume = models.CharField(max_length=100, null=True)
	quantity = models.CharField(max_length=100, null=True)
	weight = models.CharField(max_length=100, null=True)
	chance = models.CharField(max_length=100, null=True)
	rate = models.CharField(max_length=100, null=True)
	pay = models.CharField(max_length=100, null=True)

	customer = models.ForeignKey(Customer, null=False)
	freight = models.ForeignKey(Freight, on_delete=models.CASCADE, null=True, blank=True)
	start = models.ForeignKey(Warehouse, null=False, related_name='packageStart')
	finish = models.ForeignKey(Warehouse, null=False, related_name='packageFinish')

	def __unicode__(self):
		return self.id
