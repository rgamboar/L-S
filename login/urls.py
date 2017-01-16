    # -*- coding: utf-8 -*-
from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.freightIndex, name='home'),

    url(r'^password/$',  views.changePassword, name='changePassword'),

    url(r'^paquete/crear/$',  views.package, name='package'),
    url(r'^paquete/buscar/$',  views.packageSearch, name='packageSearch'),
    
    url(r'^test/$',  views.test, name='test'),
    
    url(r'^paquete/origen/$',  views.packageIndex, name='packageIndex'),
    url(r'^paquete/transito/$',  views.packageIndex, {'traveling': True}, name='packageTraveling'),
    url(r'^paquete/destino/$',  views.packageIndex, {'finish': True}, name='packageFinish'),
    url(r'^paquete/entregado/$',  views.packageIndex, {'delivered': True}, name='packageDelivered'),
    url(r'^paquete/direccion/$',  views.packageIndex, {'reciever': True}, name='packageReciever'),
    url(r'^paquete/retirar/$',  views.packageIndex, {'transmitter': True}, name='packageTransmitter'),
    url(r'^paquete/estado/$', views.packageState, name='packageState'),

    url(r'^paquete/flete/$', views.packageFreight, name='packageFreight'),
    url(r'^paquete/(?P<package_id>.*)/$', views.packageProfile, name='packageProfile'),

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

    url(r'^flete/cargar/(?P<freight_id>.*)/$', views.freightProfile, {'load': True}, name='freightProfileLoad'),
    url(r'^flete/camion/$', views.freightTruck, name='freightTruck'),
    url(r'^flete/conductor/$', views.freightDriver, name='freightDriver'),
    url(r'^flete/estado/$', views.freightState, name='freightState'),
    url(r'^flete/(?P<freight_id>.*)/$', views.freightProfile, name='freightProfile'),


    url(r'^camion/crear/$',  views.truck, name='truck'),
    url(r'^conductor/crear/$',  views.driver, name='driver'),
]

