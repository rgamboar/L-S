from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.core.urlresolvers import reverse
from .forms import *
from .models import *
from datetime import datetime
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from reportlab.pdfgen import canvas
from bson import json_util
import json

from packages.models import *
from packages.views import packageProfile
from freights.models import *
from freights.views import freightProfile
from django.core.paginator import Paginator



@login_required(login_url="login/")
def home(request, entity=None):
    if request.user.is_superuser:
        return HttpResponseRedirect(reverse('admin:index'))
    else:
        fail=False
        if request.method == 'POST':
            form = SearchIdForm(request.POST)
            form2 = SearchIdForm()
            if form.is_valid():
                data = form.cleaned_data
                entity_id = data['entity_id']
                if entity == 'package':
                    try:
                        package = Package.LogicPackage.get(id=entity_id)
                        return packageProfile(request, entity_id)
                    except Package.DoesNotExist:
                        fail=True
                elif entity == 'freight':
                    try:
                        freight = Freight.LogicFreight.get(id=entity_id)
                        return freightProfile(request, entity_id)
                    except Freight.DoesNotExist:
                        fail=True
        form = SearchIdForm()
        form2 = SearchIdForm()
        return render(request, 'intranet/home.html', {
            'formFreight': form,
            'formPackage': form2,
            'fail': fail
        })



@login_required(login_url="login/")
def help(request):
    return render(request,"intranet/help.html")


@login_required(login_url="login/")
def changePassword(request):
    if request.method == 'POST':
        success=False
        not_success = False
        user = request.user
        password = request.POST['password']
        password2 = request.POST['password2']
        if password == password2:
            user.set_password(password)
            user.save()
            success=True
        else:
            not_success=True
        return render(request, 'intranet/changePassword.html', 
            {
                'success': success,
                'not_success': not_success,
            })
    return render(request, 'intranet/changePassword.html')
    
