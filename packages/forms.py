# -*- coding: utf-8 -*-
from django import forms
from .models import *
from dal import autocomplete
from bootstrap3_datetime.widgets import DateTimePicker
from datetime import datetime


class PackageForm(forms.ModelForm):
	name = forms.CharField(label='Descripción',max_length=300, required=False)
	
	start = forms.ModelChoiceField(label='Origen',queryset=Warehouse.LogicWarehouse.all(), empty_label=None)
	startAddress = forms.CharField(label='Direccion de origen',max_length=300, required=False)
	
	finish = forms.ModelChoiceField(label='Destino',queryset=Warehouse.LogicWarehouse.all(), empty_label=None)
	finishAddress = forms.CharField(label='Direccion de destino',max_length=300, required=False)

	provider = forms.ModelChoiceField(label='Proveedor',queryset=Customer.LogicCustomer.all(), widget=autocomplete.ModelSelect2(url='customer-autocomplete'), required=False)
	consignee = forms.ModelChoiceField(label='Consignatario',queryset=Customer.LogicCustomer.all(), widget=autocomplete.ModelSelect2(url='customer-autocomplete'), required=False)

	payer = forms.TypedChoiceField(label="Cliente" ,coerce=lambda x: x =='True', choices=((True, 'Proveedor'),(False, 'Consignatario')))

	risk = forms.ChoiceField(label="Riesgo", choices=[("Bajo", "Bajo"),("Medio", "Medio"),("Alto", "Alto")])
	volume = forms.CharField(label='Volumen',max_length=100, required=False)
	quantity = forms.IntegerField(label='Cantidad')
	weight = forms.CharField(label='Peso',max_length=100, required=False)
	chance = forms.CharField(label='Oportunidad',max_length=100, required=False)
	rate = forms.IntegerField(label='Tarifado')
	pay = forms.TypedChoiceField(label="F. Pago" ,coerce=lambda x: x =='True', choices=((False, 'Contado'), (True, 'Credito')))

	is_boleta = forms.TypedChoiceField(label="Boleta o Factura?" ,coerce=lambda x: x =='True', choices=((False, 'Factura'), (True, 'Boleta')))
	boleta = forms.IntegerField(required=False, label="Numero de boleta")

	class Meta:
		model = Package
		fields = ['name','start','startAddress', 'finish','finishAddress','provider','consignee','payer' ,'risk','volume','quantity','weight','chance','rate','pay','is_boleta','boleta']



class SearchBoxForm(forms.Form):
	search = forms.CharField(label='Buscar',max_length=100, required=False)
	status = forms.ChoiceField(choices=[("5", "Todos"),("1", "Origen"),("2", "Transito"),("3", "Destino"),("4", "Entregado")])
	binicial = forms.ModelChoiceField(label='Bodega Inicial',queryset=Warehouse.LogicWarehouse.all(), required=False)
	bfinal = forms.ModelChoiceField(label='Bodega Final',queryset=Warehouse.LogicWarehouse.all(), required=False)
	rate = forms.BooleanField(label='Mostrar solo por tarifar', required=False)

	startDate = forms.DateTimeField(
		label='Creacion desde',
        required=False,
        widget=DateTimePicker(options={"format": "YYYY-MM-DD HH:mm",
                                       "pickSeconds": False
                                       }))
	finishDate = forms.DateTimeField(
		label='Hasta',
        required=False,
        widget=DateTimePicker(options={"format": "YYYY-MM-DD HH:mm",
                                       "pickSeconds": False}))
