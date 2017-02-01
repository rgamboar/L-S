    # -*- coding: utf-8 -*-
from django.conf.urls import url
from . import views

urlpatterns = [

    url(r'^cliente/completar$', views.CustomerAutocomplete.as_view(), name='customer-autocomplete',),
    url(r'^cliente/crear/$',  views.customer, name='customer'),
    url(r'^cliente/indice/$',  views.customerIndex, name='customerIndex'),
    url(r'^cliente/modificar/(?P<customer_id>.*)/$', views.customerUpdate, name='customerUpdate'),
    url(r'^cliente/buscar/$',  views.customerSearch, name='customerSearch'),
    url(r'^cliente/(?P<customer_id>.*)/$', views.customerProfile, name='customerProfile'),

]