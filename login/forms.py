# -*- coding: utf-8 -*-
from django.contrib.auth.forms import AuthenticationForm 
from django import forms
from login.models import *


# If you don't do this you cannot use Bootstrap CSS
class LoginForm(AuthenticationForm):
    username = forms.CharField(label="Nombre de usuario", max_length=30, 
                               widget=forms.TextInput(attrs={'class': 'form-control', 'name': 'username'}))
    password = forms.CharField(label="Contraseña", max_length=30, 
                               widget=forms.PasswordInput(attrs={'class': 'form-control', 'name': 'password'}))

class WarehouseForm(forms.ModelForm):
	name = forms.CharField(label='Nombre',max_length=150)
	phone = forms.CharField(label='Telefono',max_length=150)
	rep = forms.CharField(label='Encargado',max_length=150)

	class Meta:
		model = Warehouse
		fields = ['name','phone','rep']

class DriverForm(forms.ModelForm):
	name = forms.CharField(label='Nombre',max_length=150)
	phone = forms.CharField(label='Telefono',max_length=150)

	class Meta:
		model = Driver
		fields = ['name','phone',]

class TruckForm(forms.ModelForm):
	plate = forms.CharField(label='Patente',max_length=150)
	is_rent = forms.BooleanField(label='Es arrendado', required=False)

	class Meta:
		model = Truck
		fields = ['plate','is_rent']

class CustomerForm(forms.ModelForm):
	name = forms.CharField(label='Nombre',max_length=150)
	rut = forms.CharField(label='Rut',max_length=150)
	address = forms.CharField(label='Direccion',max_length=150)
	phone = forms.CharField(label='Telefono',max_length=150)

	rep = forms.CharField(label='Representante',max_length=150)
	repAddress = forms.CharField(label='Direccion representante',max_length=150)
	repEmail = forms.CharField(label='Mail representante',max_length=150)
	repPhone = forms.CharField(label='Telefono representante',max_length=150)
	pay = forms.CharField(label='Forma de pago',max_length=150)

	class Meta:
		model = Customer
		fields = ['name','rut','address','phone','rep','repAddress','repEmail','repPhone','pay']

class FreightForm(forms.ModelForm):
	start = forms.ModelChoiceField(label='Origen',queryset=Warehouse.objects.all(), empty_label=None)
	finish = forms.ModelChoiceField(label='Destino',queryset=Warehouse.objects.all(), empty_label=None)
	truck = forms.ModelChoiceField(label='Camión',queryset=Truck.objects.all(), required=False)
	driver = forms.ModelChoiceField(label='Conductor',queryset=Driver.objects.all(), required=False)

	class Meta:
		model = Freight
		fields = ['start','finish','truck','driver']

class PackageForm(forms.ModelForm):
	name = forms.CharField(label='Nombre',max_length=300)
	start = forms.ModelChoiceField(label='Origen',queryset=Warehouse.objects.all(), empty_label=None)
	finish = forms.ModelChoiceField(label='Destino',queryset=Warehouse.objects.all(), empty_label=None)
	customer = forms.ModelChoiceField(label='Cliente',queryset=Customer.objects.all(), empty_label=None)
	freight = forms.ModelChoiceField(label='Flete',queryset=Freight.objects.all(), required=False)

	risk = forms.CharField(label='Riesgo',max_length=100)
	volume = forms.CharField(label='Volumen',max_length=100)
	quantity = forms.CharField(label='Cantidad',max_length=100)
	weight = forms.CharField(label='Peso',max_length=100)
	chance = forms.CharField(label='Oportunidad',max_length=100)
	rate = forms.CharField(label='Tarifado',max_length=100)
	pay = forms.CharField(label='F. Pago',max_length=100)

	class Meta:
		model = Package
		fields = ['name','start', 'finish','customer','freight','risk','volume','quantity','weight','chance','rate','pay']
