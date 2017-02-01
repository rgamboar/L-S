# -*- coding: utf-8 -*-
from django.contrib.auth.forms import AuthenticationForm 
from django.core.exceptions import ValidationError
from django import forms
from customers.models import *

def validate_rut(value):
	dv= value[-1]
	value= value[:-1]
	try:
		rut = int(filter(unicode.isdigit, value))
	except ValueError:
		raise ValidationError(
			('No es un rut valido'),
		)
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


class CustomerForm(forms.ModelForm):
	name = forms.CharField(label='Nombre',max_length=150)
	rut = forms.CharField(label='Rut',max_length=150,validators=[validate_rut], error_messages={'unique':"Este rut ya existe en el sistema"})
	address = forms.CharField(label='Direccion',max_length=150)
	phone = forms.CharField(label='Telefono',max_length=150)

	rep = forms.CharField(label='Representante',max_length=150, required=False)
	repAddress = forms.CharField(label='Direccion representante',max_length=150, required=False)
	repEmail = forms.CharField(label='Mail representante',max_length=150, required=False)
	repPhone = forms.CharField(label='Telefono representante',max_length=150, required=False)
	pay = forms.ChoiceField(label="F. Pago", choices=[("Credito", "Credito"),("Contado", "Contado")])

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
	pay = forms.ChoiceField(label="F. Pago", choices=[("Credito", "Credito"),("Contado", "Contado")])

	class Meta:
		model = Customer
		fields = ['name','address','phone','rep','repAddress','repEmail','repPhone','pay']

class FastCustomerForm(forms.Form):
	name = forms.CharField(label='Nombre',max_length=150, required=False)
	rut = forms.CharField(label='Rut',max_length=150,validators=[validate_rut], error_messages={'unique':"Este rut ya existe en el sistema"}, required=False)
	address = forms.CharField(label='Direccion',max_length=150, required=False)
	repEmail = forms.CharField(label='Email',max_length=150, required=False)
	phone = forms.CharField(label='Telefono',max_length=150, required=False)

	def clean_rut(self):
		value = self.cleaned_data['rut']
		if not value:
			raise forms.ValidationError("")
		dv= value[-1]
		value= value[:-1]
		rut = int(filter(unicode.isdigit, value))
		return unicode(rut) + '-' + dv


class SearchCustomerForm(forms.Form):
	name = forms.CharField(label='Nombre',max_length=150, required=False)
	rut = forms.CharField(label='Rut',max_length=150, required=False)
	repEmail = forms.CharField(label='Email',max_length=150, required=False)
	phone = forms.CharField(label='Telefono',max_length=150, required=False)
