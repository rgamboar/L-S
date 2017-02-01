# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib.auth.models import User
from django.db import models



class LogicWarehouseManager(models.Manager):
    def get_queryset(self):
        return super(LogicWarehouseManager, self).get_queryset().filter(delete=False)

class LogicDriverManager(models.Manager):
    def get_queryset(self):
        return super(LogicDriverManager, self).get_queryset().filter(delete=False)

class LogicTruckManager(models.Manager):
    def get_queryset(self):
        return super(LogicTruckManager, self).get_queryset().filter(delete=False)

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

