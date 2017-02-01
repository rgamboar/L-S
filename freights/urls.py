    # -*- coding: utf-8 -*-
from django.conf.urls import url
from . import views

urlpatterns = [
    
    url(r'^flete/crear/$',  views.freight, name='freight'),
    url(r'^flete/origen/$',  views.freightIndex, name='freightIndex'),
    url(r'^flete/transito/$',  views.freightIndex, {'traveling': True}, name='freightTraveling'),
    url(r'^flete/destino/$',  views.freightIndex, {'finish': True}, name='freightFinish'),
    
    url(r'^flete/pdf/(?P<freight_id>.*)/$',  views.freightPdf, name='freightPdf'),
    
    url(r'^flete/buscar/$',  views.freightSearch, name='freightSearch'),

    url(r'^flete/cargar/(?P<freight_id>.*)/$', views.freightProfile, {'load': True}, name='freightProfileLoad'),
    url(r'^flete/camion/$', views.freightTruck, name='freightTruck'),
    url(r'^flete/conductor/$', views.freightDriver, name='freightDriver'),
    url(r'^flete/estado/$', views.freightState, name='freightState'),
    url(r'^flete/(?P<freight_id>.*)/$', views.freightProfile, name='freightProfile'),
]

