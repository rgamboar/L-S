# -*- coding: utf-8 -*-
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

class WarehouseManager(models.Manager):
	def get_by_natural_key(self, name):
		return self.get(name=name)


class Warehouse(models.Model):
	objects = WarehouseManager()

	name = models.CharField(max_length=150, null=False, unique=True, verbose_name="Nombre")
	phone = models.CharField(max_length=150, null=False, verbose_name="Telefono")
	rep = models.CharField(max_length=150, null=False, verbose_name="Representante")

	createDate = models.DateTimeField(auto_now=True, verbose_name="Fecha de creado")
	lastDate = models.DateTimeField(auto_now_add=True, verbose_name="Ultima fecha modificado")

	creator = models.ForeignKey(User, null=False, related_name='warehouseCreator', verbose_name="U. Creado")
	delete = models.BooleanField(default=False, verbose_name="Borrado")
	objects = models.Manager()
	LogicWarehouse = LogicWarehouseManager()

	def natural_key(self):
		return (self.name)

	def __unicode__(self):
		return self.name
	class Meta:
		verbose_name = 'Bodega'
		verbose_name_plural = 'Bodegas'

class Driver(models.Model):
	name = models.CharField(max_length=150, null=False, verbose_name="Nombre")
	phone = models.CharField(max_length=150, null=False, verbose_name="Telefono")

	createDate = models.DateTimeField(auto_now=True, verbose_name="Fecha de creado")
	lastDate = models.DateTimeField(auto_now_add=True, verbose_name="Ultima fecha modificado")

	creator = models.ForeignKey(User, null=False, related_name='driverCreator', verbose_name="U. Creado")
	delete = models.BooleanField(default=False, verbose_name="Borrado")
	objects = models.Manager()
	LogicDriver = LogicDriverManager()

	def __unicode__(self):
		return self.name
	class Meta:
		verbose_name = 'Conductor'
		verbose_name_plural = 'Conductores'

class Truck(models.Model):
	plate = models.CharField(max_length=150, null=False, unique=True, verbose_name="Patente")
	is_rent = models.BooleanField(null=False, verbose_name="Es arrendado?")
	createDate = models.DateTimeField(auto_now=True, verbose_name="Fecha de creado")
	lastDate = models.DateTimeField(auto_now_add=True, verbose_name="Ultima fecha modificado")
	creator = models.ForeignKey(User, null=False, related_name='truckCreator', verbose_name="U. Creado")
	delete = models.BooleanField(default=False, verbose_name="Borrado")
	objects = models.Manager()
	LogicTruck = LogicTruckManager()


	def __unicode__(self):
		return self.plate
	class Meta:
		verbose_name = 'Camión'
		verbose_name_plural = 'Camiones'


class Customer(models.Model):
	name = models.CharField(max_length=150, null=False, verbose_name="Nombre")
	rut = models.CharField(max_length=150, null=False, unique=True, verbose_name="Rut")
	address = models.CharField(max_length=150, null=False, verbose_name="Direccion")
	phone = models.CharField(max_length=150, null=False, verbose_name="Telefono")

	rep = models.CharField(max_length=150, null=True, verbose_name="Representante")
	repAddress = models.CharField(max_length=150, null=True, verbose_name="Direccion Representante")
	repEmail = models.CharField(max_length=150, null=True, verbose_name="Email Representante")
	repPhone = models.CharField(max_length=150, null=True, verbose_name="Telefono Representante")
	pay = models.CharField(max_length=150, null=False, verbose_name="Forma de pago")

	createDate = models.DateTimeField(auto_now=True, verbose_name="Fecha de creado")
	lastDate = models.DateTimeField(auto_now_add=True, verbose_name="Ultima fecha modificado")

	creator = models.ForeignKey(User, null=False, related_name='customerCreator', verbose_name="U. Creado")
	delete = models.BooleanField(default=False, verbose_name="Borrado")
	objects = models.Manager()
	LogicCustomer = LogicCustomerManager()

	def __unicode__(self):
		return self.name
	class Meta:
		verbose_name = 'Cliente'
		verbose_name_plural = 'Clientes'

class Freight(models.Model):
	createDate = models.DateTimeField(auto_now=True, verbose_name="Fecha de creado")
	sendDate = models.DateTimeField(null=True, verbose_name="Fecha de envio")
	receiveDate = models.DateTimeField(null=True, verbose_name="Fecha de recibido")
	lastDate = models.DateTimeField(auto_now_add=True, verbose_name="Ultima fecha modificado")

	is_waiting=models.BooleanField(default=True, verbose_name="Esta esperando?")
	is_traveling = models.BooleanField(default=False, verbose_name="Esta viajando?")

	start = models.ForeignKey(Warehouse, null=False, related_name='travelStart', verbose_name="Bodega inicio")
	finish = models.ForeignKey(Warehouse, null=False, related_name='travelFinish', verbose_name="Bodega destino")
	truck = models.ForeignKey(Truck, null=True, verbose_name="Camion")
	driver = models.ForeignKey(Driver, null=True, verbose_name="Conductor")

	creator = models.ForeignKey(User, null=False, related_name='freightCreator', verbose_name="U. Creado")
	sender = models.ForeignKey(User, null=True, related_name='freightSender', verbose_name="U. Envio")
	receiver = models.ForeignKey(User, null=True, related_name='freightReceiver', verbose_name="U. recibido")
	delete = models.BooleanField(default=False, verbose_name="Borrado")
	objects = models.Manager()
	LogicFreight = LogicFreightManager()

	def __unicode__(self):
		return unicode(self.id)

	def totalRate(self):
		packages= Package.LogicPackage.filter(freight=self)
		total = 0
		for package in packages:
			total = total + package.total()
		return total
	class Meta:
		verbose_name = 'Manifiesto de carga'
		verbose_name_plural = 'Manifiestos de carga'


class Package(models.Model):
	name = models.CharField(max_length=300, null=True, verbose_name="Descripción")
	lastDate = models.DateTimeField(auto_now=True, verbose_name="Ultima modificación")
	createDate = models.DateTimeField(auto_now_add=True, verbose_name="Creacion")
	deliverDate = models.DateTimeField(null=True, verbose_name="Entrega")
	transmitDate = models.DateTimeField(null=True, verbose_name="Ido a buscar")

	startAddress = models.CharField(max_length=300, null=True, verbose_name="Dirección origen")
	finishAddress = models.CharField(max_length=300, null=True, verbose_name="Dirección destino")

	is_waiting =models.BooleanField(default=True, verbose_name="Esta esperando?")
	is_traveling =models.BooleanField(default=False, verbose_name="Esta viajando?")
	is_delivered =models.BooleanField(default=False, verbose_name="Fue entregado?")
	is_transmitter =models.BooleanField(default=False, verbose_name="Ir a buscar?")
	is_receiver =models.BooleanField(default=False, verbose_name="Ir a entregar?")

	is_boleta =models.BooleanField(default=False, verbose_name="Es boleta?")
	boleta = models.IntegerField(null=True, verbose_name="Boleta")

	risk = models.CharField(max_length=100, null=True, verbose_name="Riesgo")
	volume = models.CharField(max_length=100, null=True, verbose_name="Volumen")
	quantity = models.IntegerField(null=True, verbose_name="Cantidad")
	weight = models.CharField(max_length=100, null=True, verbose_name="Peso")
	chance = models.CharField(max_length=100, null=True, verbose_name="Oportunidad")
	rate = models.IntegerField(null=False, verbose_name="Tarifado")
	credit = models.BooleanField(default=False, verbose_name="Forma de pago")

	customer = models.ForeignKey(Customer, null=False, verbose_name="Cliente", related_name='packageCustomer')
	provider = models.ForeignKey(Customer, null=False, verbose_name="Prooveedor", related_name='packageProvider')
	consignee = models.ForeignKey(Customer, null=False, verbose_name="Consignatario", related_name='packageConsignee')
	payer = models.BooleanField(default=False, verbose_name="Paga el proveedor?")

	freight = models.ForeignKey(Freight, on_delete=models.CASCADE, null=True, blank=True, verbose_name="Manifiesto de carga")
	start = models.ForeignKey(Warehouse, null=False, related_name='packageStart', verbose_name="Origen")
	finish = models.ForeignKey(Warehouse, null=False, related_name='packageFinish', verbose_name="Destino")
	
	creator = models.ForeignKey(User, null=False, related_name='packageCreator', verbose_name="U. Creado")
	deliverer = models.ForeignKey(User, null=True, related_name='packageDeliverer', verbose_name="U. Entregado")
	transmitter = models.ForeignKey(User, null=True, related_name='packageTransmitter', verbose_name="U. Ir a buscar")
	delete = models.BooleanField(default=False, verbose_name="Borrado")
	objects = models.Manager()
	LogicPackage = LogicPackageManager()

	class Meta:
		ordering = ['-createDate']
		verbose_name = 'Guia de flete'
		verbose_name_plural = 'Guias de flete'
	
	def __unicode__(self):
		return unicode(self.id)

	def total(self):
		return self.quantity*self.rate
