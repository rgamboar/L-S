from django.shortcuts import render
from django.contrib.auth.models import User
from .forms import *
from .models import *
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator


@login_required(login_url="login/")
def warehouse(request):
    success=False
    warehouses = Warehouse.LogicWarehouse.all()
    if request.method == 'POST':
        form = WarehouseForm(request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.creator = request.user
            obj.save()
            success=True
    else:
        form = WarehouseForm()
    return render(request, 'intranet/warehouse.html', {
        'form': form,
        'success': success,
        'warehouses': warehouses
    })

@login_required(login_url="login/")
def truck(request):
    success=False
    trucks = Truck.LogicTruck.all()
    if request.method == 'POST':
        form = TruckForm(request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.creator = request.user
            obj.save()
            success=True
    else:
        form = TruckForm()
    return render(request, 'intranet/truck.html', {
        'form': form,
        'success': success,
        'trucks' : trucks
    })

@login_required(login_url="login/")
def driver(request):
    success=False
    drivers = Driver.LogicDriver.all()
    if request.method == 'POST':
        form = DriverForm(request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.creator = request.user
            obj.save()
            success=True
    else:
        form = DriverForm()
    return render(request, 'intranet/driver.html', {
        'form': form,
        'success': success,
        'drivers': drivers
    })

