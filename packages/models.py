# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib.auth.models import User
from django.db import models
from intranet.models import *
from customers.models import *

class LogicPackageManager(models.Manager):
    def get_queryset(self):
        return super(LogicPackageManager, self).get_queryset().filter(delete=False)

class Package(models.Model):
	name = models.CharField(max_length=300, null=True, verbose_name="Descripción")
	lastDate = models.DateTimeField(auto_now=True, verbose_name="Ultima modificación")
	createDate = models.DateTimeField(auto_now_add=True, verbose_name="Creacion")
	deliverDate = models.DateTimeField(null=True, verbose_name="Entrega")

	finishAddress = models.CharField(max_length=300, null=True, verbose_name="Dirección destino")

	is_waiting =models.BooleanField(default=True, verbose_name="Esta esperando?")
	is_traveling =models.BooleanField(default=False, verbose_name="Esta viajando?")
	is_delivered =models.BooleanField(default=False, verbose_name="Fue entregado?")
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

	freight = models.ForeignKey('freights.Freight', on_delete=models.CASCADE, null=True, blank=True, verbose_name="Manifiesto de carga")
	start = models.ForeignKey(Warehouse, null=False, related_name='packageStart', verbose_name="Origen")
	finish = models.ForeignKey(Warehouse, null=False, related_name='packageFinish', verbose_name="Destino")
	
	creator = models.ForeignKey(User, null=False, related_name='packageCreator', verbose_name="U. Creado")
	deliverer = models.ForeignKey(User, null=True, related_name='packageDeliverer', verbose_name="U. Entregado")
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
