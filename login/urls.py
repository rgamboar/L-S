    # -*- coding: utf-8 -*-
from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^guia/$',  views.help, name='help'),
    url(r'^password/$',  views.changePassword, name='changePassword'),

    url(r'^accounts/profile/$',  views.home, name='adminAcount'),



    url(r'^buscar/manifiesto/$', views.home, {'entity': 'freight'}, name='homeFreight'),
    url(r'^buscar/guia/$', views.home, {'entity': 'package'}, name='homePackage'),

]

