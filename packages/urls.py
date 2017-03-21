    # -*- coding: utf-8 -*-
from django.conf.urls import url
from . import views

urlpatterns = [


    url(r'^guia/crear/$',  views.package, name='package'),
    url(r'^guia/modificar/$',  views.packageChange, name='packageChange'),
    url(r'^guia/buscar/$',  views.packageSearch, name='packageSearch'),
    
    url(r'^guia/origen/$',  views.packageIndex, name='packageIndex'),
    url(r'^guia/transito/$',  views.packageIndex, {'traveling': True}, name='packageTraveling'),
    url(r'^guia/destino/$',  views.packageIndex, {'finish': True}, name='packageFinish'),
    url(r'^guia/entregado/$',  views.packageIndex, {'delivered': True}, name='packageDelivered'),
    url(r'^guia/direccion/$',  views.packageIndex, {'reciever': True}, name='packageReciever'),
    url(r'^guia/retirar/$',  views.packageIndex, {'transmitter': True}, name='packageTransmitter'),
    url(r'^guia/estado/$', views.packageState, name='packageState'),
    url(r'^guia/tarifado/$', views.packageRate, name='packageRate'),
    url(r'^guia/formadepago/$', views.packagePay, name='packagePay'),

    url(r'^guia/pdf/(?P<package_id>.*)/$',  views.packagePdf, name='packagePdf'),

    url(r'^guia/flete/$', views.packageFreight, name='packageFreight'),
    url(r'^guia/(?P<package_id>.*)/$', views.packageProfile, name='packageProfile'),

    url(r'^recogida/crear/$',  views.pickup, name='pickup'),   
    url(r'^recogida/esperando/$',  views.pickupWaiting, name='pickupWaiting'),
    url(r'^recogida/listos/$',  views.pickupReady , name='pickupReady'),
    url(r'^recogida/guia/$',  views.pickupPackage, name='pickupPackage'),
    url(r'^recogida/(?P<pickup_id>.*)/$',  views.pickupProfile, name='pickupProfile'),

]

