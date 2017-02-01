# -*- coding: utf-8 -*-
from django import forms
from .models import *


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
