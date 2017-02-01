"""LS URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from django.contrib.auth import views
from login.forms import LoginForm


urlpatterns = [

    url(r'^admin/', admin.site.urls, name='admin'),
    url(r'', include('login.urls')),
    url(r'', include('customers.urls')),
    url(r'', include('freights.urls')),
    url(r'', include('intranet.urls')),
    url(r'', include('packages.urls')),
    url(r'^login/$', views.login, {'template_name': 'intranet/login.html', 'authentication_form': LoginForm} , name='login'),  
    url(r'^logout/$', views.logout, {'next_page': '/login'}, name='logout'),  
]