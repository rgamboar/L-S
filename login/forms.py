# -*- coding: utf-8 -*-
from django.contrib.auth.forms import AuthenticationForm 
from django.core.exceptions import ValidationError
from django import forms
from login.models import *


class LoginForm(AuthenticationForm):
    username = forms.CharField(label="Nombre de usuario", max_length=30, 
                               widget=forms.TextInput(attrs={'class': 'form-control', 'name': 'username'}))
    password = forms.CharField(label="Contraseña", max_length=30, 
                               widget=forms.PasswordInput(attrs={'class': 'form-control', 'name': 'password'}))

def validate_rut(value):
	dv= value[-1]
	value= value[:-1]
	rut = int(filter(unicode.isdigit, value))
	add= 0
	y = 2
	for x in range ( 1 , 20):
		loop = (rut%10)
		add = add + loop * y
		y= y+1
		if (y==8):
			y=2
		rut = rut/10
	check = 11-(add%11)
	error=True
	if check==10:
		if dv == 'k' or dv =='K':
			error=False
	else:
		if int(dv) == check:
			error=False
	if error:
		raise ValidationError(
			('No es un rut valido'),
		)

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
	rut = forms.CharField(label='Rut',max_length=150,validators=[validate_rut], error_messages={'unique':"Este rut ya existe en el sistema"})
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

	def clean_rut(self):
		value = self.cleaned_data['rut']
		dv= value[-1]
		value= value[:-1]
		rut = int(filter(unicode.isdigit, value))
		return unicode(rut) + '-' + dv

class CustomerFormUpdate(forms.ModelForm):
	name = forms.CharField(label='Nombre',max_length=150)
	address = forms.CharField(label='Direccion',max_length=150)
	phone = forms.CharField(label='Telefono',max_length=150)

	rep = forms.CharField(label='Representante',max_length=150)
	repAddress = forms.CharField(label='Direccion representante',max_length=150)
	repEmail = forms.CharField(label='Mail representante',max_length=150)
	repPhone = forms.CharField(label='Telefono representante',max_length=150)
	pay = forms.CharField(label='Forma de pago',max_length=150)

	class Meta:
		model = Customer
		fields = ['name','address','phone','rep','repAddress','repEmail','repPhone','pay']


class FreightForm(forms.ModelForm):
	start = forms.ModelChoiceField(label='Origen',queryset=Warehouse.LogicWarehouse.all(), empty_label=None)
	finish = forms.ModelChoiceField(label='Destino',queryset=Warehouse.LogicWarehouse.all(), empty_label=None)
	truck = forms.ModelChoiceField(label='Camión',queryset=Truck.LogicTruck.all(), required=False)
	driver = forms.ModelChoiceField(label='Conductor',queryset=Driver.LogicDriver.all(), required=False)

	class Meta:
		model = Freight
		fields = ['start','finish','truck','driver']

class PackageForm(forms.ModelForm):
	name = forms.CharField(label='Nombre',max_length=300)
	
	start = forms.ModelChoiceField(label='Origen',queryset=Warehouse.LogicWarehouse.all(), empty_label=None)
	startAddress = forms.CharField(label='Direccion de origen',max_length=300, required=False)
	
	finish = forms.ModelChoiceField(label='Destino',queryset=Warehouse.LogicWarehouse.all(), empty_label=None)
	finishAddress = forms.CharField(label='Direccion de destino',max_length=300, required=False)

	customer = forms.ModelChoiceField(label='Cliente',queryset=Customer.LogicCustomer.all(), empty_label=None)

	risk = forms.CharField(label='Riesgo',max_length=100)
	volume = forms.CharField(label='Volumen',max_length=100)
	quantity = forms.CharField(label='Cantidad',max_length=100)
	weight = forms.CharField(label='Peso',max_length=100)
	chance = forms.CharField(label='Oportunidad',max_length=100)
	rate = forms.CharField(label='Tarifado',max_length=100)
	pay = forms.CharField(label='F. Pago',max_length=100)

	class Meta:
		model = Package
		fields = ['name','start','startAddress', 'finish','finishAddress','customer','risk','volume','quantity','weight','chance','rate','pay']

class ChangePasswordForm(forms.ModelForm):
    password = forms.CharField(label="Contraseña", max_length=30, 
                               widget=forms.PasswordInput(attrs={'class': 'form-control', 'name': 'password'}))
    password2 = forms.CharField(label="Repetir contraseña", max_length=30, 
                               widget=forms.PasswordInput(attrs={'class': 'form-control', 'name': 'password2'}))
