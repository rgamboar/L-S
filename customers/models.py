from __future__ import unicode_literals
from django.contrib.auth.models import User
from django.db import models

class LogicCustomerManager(models.Manager):
    def get_queryset(self):
        return super(LogicCustomerManager, self).get_queryset().filter(delete=False)

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
