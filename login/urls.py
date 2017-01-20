    # -*- coding: utf-8 -*-
from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.freightIndex, name='home'),

    url(r'^password/$',  views.changePassword, name='changePassword'),
    url(r'^guia/$',  views.help, name='help'),

    url(r'^guia/crear/$',  views.package, name='package'),
    url(r'^guia/buscar/$',  views.packageSearch, name='packageSearch'),
    
    url(r'^guia/origen/$',  views.packageIndex, name='packageIndex'),
    url(r'^guia/transito/$',  views.packageIndex, {'traveling': True}, name='packageTraveling'),
    url(r'^guia/destino/$',  views.packageIndex, {'finish': True}, name='packageFinish'),
    url(r'^guia/entregado/$',  views.packageIndex, {'delivered': True}, name='packageDelivered'),
    url(r'^guia/direccion/$',  views.packageIndex, {'reciever': True}, name='packageReciever'),
    url(r'^guia/retirar/$',  views.packageIndex, {'transmitter': True}, name='packageTransmitter'),
    url(r'^guia/estado/$', views.packageState, name='packageState'),
    url(r'^guia/tarifado/$', views.packageRate, name='packageRate'),

    url(r'^guia/flete/$', views.packageFreight, name='packageFreight'),
    url(r'^guia/(?P<package_id>.*)/$', views.packageProfile, name='packageProfile'),

    url(r'^accounts/profile/$',  views.home, name='adminAcount'),

    url(r'^bodega/crear/$',  views.warehouse, name='warehouse'),

    url(r'^cliente/crear/$',  views.customer, name='customer'),
    url(r'^cliente/indice/$',  views.customerIndex, name='customerIndex'),
    url(r'^cliente/modificar/(?P<customer_id>.*)/$', views.customerUpdate, name='customerUpdate'),
    url(r'^cliente/(?P<customer_id>.*)/$', views.customerProfile, name='customerProfile'),


    url(r'^flete/crear/$',  views.freight, name='freight'),
    url(r'^flete/origen/$',  views.freightIndex, name='freightIndex'),
    url(r'^flete/transito/$',  views.freightIndex, {'traveling': True}, name='freightTraveling'),
    url(r'^flete/destino/$',  views.freightIndex, {'finish': True}, name='freightFinish'),
    
    url(r'^flete/pdf/(?P<freight_id>.*)/$',  views.freightPdf, name='freightPdf'),
    
    url(r'^flete/test/$',  views.freightPdf, name='freightPdf'),
    

    url(r'^flete/cargar/(?P<freight_id>.*)/$', views.freightProfile, {'load': True}, name='freightProfileLoad'),
    url(r'^flete/camion/$', views.freightTruck, name='freightTruck'),
    url(r'^flete/conductor/$', views.freightDriver, name='freightDriver'),
    url(r'^flete/estado/$', views.freightState, name='freightState'),
    url(r'^flete/(?P<freight_id>.*)/$', views.freightProfile, name='freightProfile'),


    url(r'^camion/crear/$',  views.truck, name='truck'),
    url(r'^conductor/crear/$',  views.driver, name='driver'),
]

