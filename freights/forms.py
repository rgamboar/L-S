# -*- coding: utf-8 -*-
from django import forms
from .models import *
from bootstrap3_datetime.widgets import DateTimePicker
from datetime import datetime

class FreightForm(forms.ModelForm):
	start = forms.ModelChoiceField(label='Origen',queryset=Warehouse.LogicWarehouse.all(), empty_label=None)
	finish = forms.ModelChoiceField(label='Destino',queryset=Warehouse.LogicWarehouse.all(), empty_label=None)
	truck = forms.ModelChoiceField(label='Camión',queryset=Truck.LogicTruck.all(), required=False)
	driver = forms.ModelChoiceField(label='Conductor',queryset=Driver.LogicDriver.all(), required=False)

	class Meta:
		model = Freight
		fields = ['start','finish','truck','driver']


class SearchFreightForm(forms.Form):
	status = forms.ChoiceField(label='Status', choices=[("4", "Todos"),("1", "Origen"),("2", "Transito"),("3", "Destino")])
	binicial = forms.ModelChoiceField(label='Bodega Inicial',queryset=Warehouse.LogicWarehouse.all(), required=False)
	bfinal = forms.ModelChoiceField(label='Bodega Final',queryset=Warehouse.LogicWarehouse.all(), required=False)

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

