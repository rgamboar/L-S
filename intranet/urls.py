    # -*- coding: utf-8 -*-
from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^bodega/crear/$',  views.warehouse, name='warehouse'),
    url(r'^camion/crear/$',  views.truck, name='truck'),
    url(r'^conductor/crear/$',  views.driver, name='driver'),
]

