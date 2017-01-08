from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.freightIndex, name='home'),

    url(r'^paquete/crear/$',  views.package, name='package'),
    url(r'^paquete/inicio/$',  views.packageIndex, name='packageIndex'),
    url(r'^paquete/flete/$', views.packageFreight, name='packageFreight'),
    url(r'^paquete/(?P<package_id>.*)/$', views.packageProfile, name='packageProfile'),



    url(r'^accounts/profile/$',  views.home, name='adminAcount'),

    url(r'^bodega/crear/$',  views.warehouse, name='warehouse'),

    url(r'^cliente/crear/$',  views.customer, name='customer'),

    url(r'^flete/crear/$',  views.freight, name='freight'),
    url(r'^flete/inicio/$',  views.freightIndex, name='freightIndex'),
    url(r'^flete/cargar/(?P<freight_id>.*)/$', views.freightProfile, {'load': True}, name='freightProfileLoad'),
    url(r'^flete/(?P<freight_id>.*)/$', views.freightProfile, name='freightProfile'),

    url(r'^camion/crear/$',  views.truck, name='truck'),
    url(r'^conductor/crear/$',  views.driver, name='driver'),
]

