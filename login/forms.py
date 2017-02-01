# -*- coding: utf-8 -*-
from django.contrib.auth.forms import AuthenticationForm 
from django.core.exceptions import ValidationError
from django import forms
from login.models import *
from django.contrib.admin import widgets                                       
from bootstrap3_datetime.widgets import DateTimePicker
from datetime import datetime
from dal import autocomplete



class LoginForm(AuthenticationForm):
    username = forms.CharField(label="Nombre de usuario", max_length=30, 
                               widget=forms.TextInput(attrs={'class': 'form-control', 'name': 'username'}))
    password = forms.CharField(label="Contraseña", max_length=30, 
                               widget=forms.PasswordInput(attrs={'class': 'form-control', 'name': 'password'}))



class SearchIdForm(forms.Form):
	entity_id = forms.IntegerField(label='ID', required=True)