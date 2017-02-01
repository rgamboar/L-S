# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib.auth.models import User
from django.db import models
from intranet.models import *
from packages.models import *



class LogicFreightManager(models.Manager):
    def get_queryset(self):
        return super(LogicFreightManager, self).get_queryset().filter(delete=False)

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
