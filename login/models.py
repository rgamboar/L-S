from __future__ import unicode_literals
from django.contrib.auth.models import User
from django.db import models

# Create your models here.


class LogicWarehouseManager(models.Manager):
    def get_queryset(self):
        return super(LogicWarehouseManager, self).get_queryset().filter(delete=False)

class LogicDriverManager(models.Manager):
    def get_queryset(self):
        return super(LogicDriverManager, self).get_queryset().filter(delete=False)

class LogicTruckManager(models.Manager):
    def get_queryset(self):
        return super(LogicTruckManager, self).get_queryset().filter(delete=False)

class LogicCustomerManager(models.Manager):
    def get_queryset(self):
        return super(LogicCustomerManager, self).get_queryset().filter(delete=False)

class LogicFreightManager(models.Manager):
    def get_queryset(self):
        return super(LogicFreightManager, self).get_queryset().filter(delete=False)

class LogicPackageManager(models.Manager):
    def get_queryset(self):
        return super(LogicPackageManager, self).get_queryset().filter(delete=False)


class Warehouse(models.Model):
	name = models.CharField(max_length=150, null=False, unique=True)
	phone = models.CharField(max_length=150, null=False)
	rep = models.CharField(max_length=150, null=False)

	createDate = models.DateTimeField(auto_now=True)
	lastDate = models.DateTimeField(auto_now_add=True)

	creator = models.ForeignKey(User, null=False, related_name='warehouseCreator')
	delete = models.BooleanField(default=False)
	LogicWarehouse = LogicWarehouseManager()

	def __unicode__(self):
		return self.name


class Driver(models.Model):
	name = models.CharField(max_length=150, null=False)
	phone = models.CharField(max_length=150, null=False)

	createDate = models.DateTimeField(auto_now=True)
	lastDate = models.DateTimeField(auto_now_add=True)

	creator = models.ForeignKey(User, null=False, related_name='driverCreator')
	delete = models.BooleanField(default=False)
	LogicDriver = LogicDriverManager()

	def __unicode__(self):
		return self.name

class Truck(models.Model):
	plate = models.CharField(max_length=150, null=False, unique=True)
	is_rent = models.BooleanField(null=False)

	createDate = models.DateTimeField(auto_now=True)
	lastDate = models.DateTimeField(auto_now_add=True)

	creator = models.ForeignKey(User, null=False, related_name='truckCreator')
	delete = models.BooleanField(default=False)
	LogicTruck = LogicTruckManager()

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

	creator = models.ForeignKey(User, null=False, related_name='customerCreator')
	delete = models.BooleanField(default=False)
	LogicCustomer = LogicCustomerManager()

	def __unicode__(self):
		return self.name

class Freight(models.Model):
	authorName= models.CharField(max_length=300, null=False)
	createDate = models.DateTimeField(auto_now=True)
	sendDate = models.DateTimeField(null=True)
	receiveDate = models.DateTimeField(null=True)
	lastDate = models.DateTimeField(auto_now_add=True)

	is_waiting=models.BooleanField(default=True)
	is_traveling = models.BooleanField(default=False)

	start = models.ForeignKey(Warehouse, null=False, related_name='travelStart')
	finish = models.ForeignKey(Warehouse, null=False, related_name='travelFinish')
	truck = models.ForeignKey(Truck, null=True)
	driver = models.ForeignKey(Driver, null=True)

	creator = models.ForeignKey(User, null=False, related_name='freightCreator')
	sender = models.ForeignKey(User, null=True, related_name='freightSender')
	receiver = models.ForeignKey(User, null=True, related_name='freightReceiver')
	delete = models.BooleanField(default=False)
	LogicFreight = LogicFreightManager()

	def __unicode__(self):
		return unicode(self.id)

	def totalRate(self):
		packages= Package.LogicPackage.filter(freight=self)
		total = 0
		for package in packages:
			total = total + package.rate
		return total


class Package(models.Model):
	name = models.CharField(max_length=300, null=True)
	authorName= models.CharField(max_length=300, null=False)
	address= models.CharField(max_length=300, null=True)
	lastDate = models.DateTimeField(auto_now=True)
	createDate = models.DateTimeField(auto_now_add=True)
	deliverDate = models.DateTimeField(null=True)
	transmitDate = models.DateTimeField(null=True)

	startAddress = models.CharField(max_length=300, null=True)
	finishAddress = models.CharField(max_length=300, null=True)

	is_waiting =models.BooleanField(default=True)
	is_traveling =models.BooleanField(default=False)
	is_delivered =models.BooleanField(default=False)
	is_transmitter =models.BooleanField(default=False)
	is_receiver =models.BooleanField(default=False)


	risk = models.CharField(max_length=100, null=True)
	volume = models.CharField(max_length=100, null=True)
	quantity = models.CharField(max_length=100, null=True)
	weight = models.CharField(max_length=100, null=True)
	chance = models.CharField(max_length=100, null=True)
	rate = models.IntegerField(null=False)
	pay = models.CharField(max_length=100, null=True)

	customer = models.ForeignKey(Customer, null=False)
	freight = models.ForeignKey(Freight, on_delete=models.CASCADE, null=True, blank=True)
	start = models.ForeignKey(Warehouse, null=False, related_name='packageStart')
	finish = models.ForeignKey(Warehouse, null=False, related_name='packageFinish')
	
	creator = models.ForeignKey(User, null=False, related_name='packageCreator')
	deliverer = models.ForeignKey(User, null=True, related_name='packageDeliverer')
	transmitter = models.ForeignKey(User, null=True, related_name='packageTransmitter')
	delete = models.BooleanField(default=False)
	LogicPackage = LogicPackageManager()

	class Meta:
		ordering = ['-id']
	
	
	def __unicode__(self):
		return unicode(self.id)

