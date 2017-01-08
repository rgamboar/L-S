from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.core.urlresolvers import reverse
from .forms import *
from .models import *

@login_required(login_url="login/")
def home(request):
	if request.user.is_superuser:
		return HttpResponseRedirect('admin')
	else:
	    return render(request,"intranet/home.html")

@login_required(login_url="login/")
def warehouse(request):
    if request.method == 'POST':
        form = WarehouseForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/')
    else:
        form = WarehouseForm()
    return render(request, 'intranet/warehouse.html', {'form': form})

@login_required(login_url="login/")
def package(request):
    if request.method == 'POST':
        form = PackageForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/')
    else:
        form = PackageForm()
    return render(request, 'intranet/package.html', {'form': form})

@login_required(login_url="login/")
def customer(request):
    if request.method == 'POST':
        form = CustomerForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/')
    else:
        form = CustomerForm()
    return render(request, 'intranet/customer.html', {'form': form})

@login_required(login_url="login/")
def freight(request):
    if request.method == 'POST':
        form = FreightForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/')
    else:
        form = FreightForm()
    return render(request, 'intranet/freights/create.html', {'form': form})

@login_required(login_url="login/")
def truck(request):
    if request.method == 'POST':
        form = TruckForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/')
    else:
        form = TruckForm()
    return render(request, 'intranet/truck.html', {'form': form})

@login_required(login_url="login/")
def driver(request):
    if request.method == 'POST':
        form = DriverForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/')
    else:
        form = DriverForm()
    return render(request, 'intranet/driver.html', {'form': form})

@login_required(login_url="login/")
def freightIndex(request):
    if request.method == 'POST':
        form = DriverForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/')
    else:
        freights = Freight.objects.all()
    return render(request, 'intranet/freights/index.html', 
        {
            'freights': freights,
        })

@login_required(login_url="login/")
def freightProfile(request, freight_id, load=False):
    if load:
        if request.method == 'POST':
            form = DriverForm(request.POST)
            if form.is_valid():
                form.save()
                return HttpResponseRedirect('/')
        else:
            freight = Freight.objects.get(id=freight_id)
            own_packages = Package.objects.filter(freight=freight)
            packages = Package.objects.filter(start=freight.start, finish= freight.finish, is_waiting= True)
            packages = packages.exclude(freight=freight_id)

        return render(request, 'intranet/freights/profile.html', 
            {
                'freight': freight,
                'packages' : packages,
                'own_packages' : own_packages,

            })
    else:
        if request.method == 'POST':
            form = DriverForm(request.POST)
            if form.is_valid():
                form.save()
                return HttpResponseRedirect('/')
        else:
            freight = Freight.objects.get(id=freight_id)
            own_packages = Package.objects.filter(freight=freight)

        return render(request, 'intranet/freights/profile.html', 
            {
                'freight': freight,
                'own_packages' : own_packages,
                'send' : True,

            })