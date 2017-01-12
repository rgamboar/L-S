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
    success=False
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
        'success': success
    })

@login_required(login_url="login/")
def package(request):
    success=False
    if request.method == 'POST':
        form = PackageForm(request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            if obj.startAddress:
                obj.is_waiting=False
                obj.is_transmitter=True
            if obj.finishAddress:
                obj.is_reciever=True
            obj.creator = request.user
            obj.save()
    else:
        form = PackageForm()
    return render(request, 'intranet/packages/create.html', {
        'form': form,
        'success': success
    })


@login_required(login_url="login/")
def packageIndex(request, traveling=False, finish=False, delivered=False, transmitter=False, reciever=False):
    if traveling:
        packages = Package.LogicPackage.filter(is_traveling=True)
        page = "traveling"
    elif finish:
        packages= Package.LogicPackage.filter(is_waiting=False, is_traveling=False, is_delivered=False, is_transmitter=False, is_receiver=False)
        page = "finish"
    elif transmitter:
        packages= Package.LogicPackage.filter(is_waiting=False, is_traveling=False, is_delivered=False, is_transmitter=True)
        page = "transmitter"
    elif delivered:
        packages= Package.LogicPackage.filter(is_waiting=False, is_traveling=False, is_delivered=True)
        page = "delivered"
    elif reciever:
        packages= Package.LogicPackage.filter(is_waiting=False, is_traveling=False, is_delivered=False, is_receiver=True)
        page = "reciever"
    else:
        packages = Package.LogicPackage.filter(is_waiting=True)
        for i in packages:
            i.posibleFreight= Freight.LogicFreight.filter(start=i.start, finish= i.finish, is_waiting= True)
            if i.freight:
                i.posibleFreight = i.posibleFreight.exclude(id= i.freight.id)
        page = "inicio"

    return render(request, 'intranet/packages/index.html', 
        {
            'packages': packages,
            'page': page,
        })

@login_required(login_url="login/")
def packageProfile(request, package_id):
    package = Package.LogicPackage.get(id=package_id)
    own_packages = Package.LogicPackage.filter(package=package)
    packages = Package.LogicPackage.filter(start=package.start, finish= package.finish, is_waiting= True)
    packages = packages.exclude(package=package_id)
    return render(request, 'intranet/packages/profile.html', 
        {
            'package': package,
            'packages' : packages,
            'own_packages' : own_packages,

        })


@login_required(login_url="login/")
def packageProfile(request, package_id):
    package = Package.LogicPackage.get(id=package_id)
    if package.is_waiting:
        return packageProfileWaiting(request, package)
    elif package.is_traveling:
        return packageProfileTraveling(request, package)
    elif package.is_delivered:
        return packageProfileDelivered(request, package)
    elif package.is_transmitter:
        return packageProfileTransmitter(request, package)
    elif package.is_receiver:
        return packageProfileTraveling(request, package)
    else:
        return packageProfileFinish(request, package)


@login_required(login_url="login/")
def packageProfileFinish(request, package):
    return render(request, 'intranet/packages/profileFinish.html', 
        {
            'package': package,
        })

@login_required(login_url="login/")
def freightProfileTraveling(request, package):
    return render(request, 'intranet/packages/profile.html', 
        {
            'package': package,
        })

@login_required(login_url="login/")
def packageProfileTransmitter(request, package):
    return render(request, 'intranet/packages/profile.html', 
        {
            'package': package,
        })

@login_required(login_url="login/")
def packageProfileDelivered(request, package):
    return render(request, 'intranet/packages/profile.html', 
        {
            'package': package,
        })


@login_required(login_url="login/")
def packageProfileTraveling(request, package):
    return render(request, 'intranet/packages/profileTraveling.html', 
        {
            'package': package,
        })


@login_required(login_url="login/")
def packageProfileWaiting(request, package):
    return render(request, 'intranet/packages/profile.html', 
        {
            'package': package,
        })



@login_required(login_url="login/")   
def packageFreight(request):
    if request.method == "POST":
        if request.is_ajax():
            package = Package.LogicPackage.get(id=request.POST['id'])
            if package.is_waiting== False:
                return JsonResponse({'error': True})
            temp= request.POST['freight']
            if temp == '-':
                freight = None
            else:
                freight = Freight.LogicFreight.get(id=temp)
                if freight.is_waiting== False:
                    return JsonResponse({'error': True})
            package.freight = freight

            package.save()
            return JsonResponse({'error': False})
        else:
            return packageIndex(request)


@login_required(login_url="login/")
def customer(request):
    success=False
    if request.method == 'POST':
        form = CustomerForm(request.POST)

        if form.is_valid():
            obj = form.save(commit=False)
            obj.creator = request.user
            obj.save()
            success=True
    else:
        form = CustomerForm()
    return render(request, 'intranet/customers/create.html', {
        'form': form,
        'success': success
    })


@login_required(login_url="login/")
def customerIndex(request):

    customers = Customer.LogicCustomer.filter()

    return render(request, 'intranet/customers/index.html', 
        {
            'customers': customers,
        })

@login_required(login_url="login/")
def customerProfile(request, customer_id):
    customer = Customer.LogicCustomer.get(id=customer_id)
    own_packages = Package.LogicPackage.filter(customer=customer)
    return render(request, 'intranet/customers/profile.html', 
        {
            'customer': customer,
            'own_packages' : own_packages,
        })


@login_required(login_url="login/")
def truck(request):
    success=False
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
        'success': success
    })

@login_required(login_url="login/")
def driver(request):
    success=False
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
        'success': success
    })


@login_required(login_url="login/")
def freight(request):
    success=False
    if request.method == 'POST':
        form = FreightForm(request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.creator = request.user
            obj.save()
            success=True
    else:
        form = FreightForm()
    return render(request, 'intranet/freights/create.html', {
        'form': form,
        'success': success
    })


@login_required(login_url="login/")
def freightIndex(request, traveling=False, finish=False):
    if traveling:
        freights = Freight.LogicFreight.filter(is_traveling=True)
        page = "traveling"
    elif finish:
        freights= Freight.LogicFreight.filter(is_waiting=False, is_traveling=False)
        page = "finish"
    else:
        freights= Freight.LogicFreight.filter(is_waiting=True)
        for freight in freights:
            freight.posibleDriver = Driver.LogicDriver.all()
            freight.posibleTruck= Truck.LogicTruck.all()
            if freight.driver:
                freight.posibleDriver = freight.posibleDriver.exclude(id=freight.driver.id)
            if freight.truck:
                freight.posibleTruck= freight.posibleTruck.exclude(id=freight.truck.id)
        page = "inicio"

    return render(request, 'intranet/freights/index.html', 
        {
            'freights': freights,
            'page': page,
        })

@login_required(login_url="login/")
def freightProfile(request, freight_id, load=False):
    freight = Freight.LogicFreight.get(id=freight_id)
    if freight.is_waiting:
        return freightProfileWaiting(request, freight, load)
    elif freight.is_traveling:
        return freightProfileTraveling(request, freight)
    else:
        return freightProfileFinish(request, freight)


@login_required(login_url="login/")
def freightProfileFinish(request, freight):
    own_packages = Package.LogicPackage.filter(freight=freight)
    return render(request, 'intranet/freights/profileFinish.html', 
        {
            'freight': freight,
            'own_packages' : own_packages,
        })

@login_required(login_url="login/")
def freightProfileTraveling(request, freight):
    own_packages = Package.LogicPackage.filter(freight=freight)
    return render(request, 'intranet/freights/profileTraveling.html', 
        {
            'freight': freight,
            'own_packages' : own_packages,
        })


@login_required(login_url="login/")
def freightProfileWaiting(request, freight, load):
    if load:
        own_packages = Package.LogicPackage.filter(freight=freight)
        packages = Package.LogicPackage.filter(start=freight.start, finish= freight.finish, is_waiting= True)
        packages = packages.exclude(freight=freight)
        
        freight.posibleDriver = Driver.LogicDriver.all()
        freight.posibleTruck= Truck.LogicTruck.all()
        if freight.driver:
            freight.posibleDriver = freight.posibleDriver.exclude(id=freight.driver.id)
        if freight.truck:
            freight.posibleTruck= freight.posibleTruck.exclude(id=freight.truck.id)
        return render(request, 'intranet/freights/profile.html', 
            {
                'freight': freight,
                'packages' : packages,
                'own_packages' : own_packages,

            })
    else:
        own_packages = Package.LogicPackage.filter(freight=freight)
        freight.posibleDriver = Driver.LogicDriver.all()
        freight.posibleTruck= Truck.LogicTruck.all()
        if freight.driver:
            freight.posibleDriver = freight.posibleDriver.exclude(id=freight.driver.id)
        if freight.truck:
            freight.posibleTruck= freight.posibleTruck.exclude(id=freight.truck.id)
        return render(request, 'intranet/freights/profile.html', 
            {
                'freight': freight,
                'own_packages' : own_packages,
                'send' : True,

            })

@login_required(login_url="login/")   
def freightDriver(request):
    if request.method == "POST":
        if request.is_ajax():
            freight = Freight.LogicFreight.get(id=request.POST['id'])
            temp= request.POST['driver']
            if temp == '-':
                driver = None
            else:
                driver = Driver.LogicDriver.get(id=temp)
            freight.driver = driver

            freight.save()
            return JsonResponse({'error': False})
        else:
            return freightIndex(request)

@login_required(login_url="login/")   
def freightState(request):
    if request.method == "POST":
        if request.is_ajax():
            freight = Freight.LogicFreight.get(id=request.POST['id'])
            temp= request.POST['state']
            if temp == 'traveling':
                freight.is_traveling = True
                freight.is_waiting = False
            elif temp == 'finish':
                freight.is_traveling= False
                freight.is_waiting= False
            packages = Package.LogicPackage.filter(freight=freight)
            for p in packages:
                p.is_waiting=freight.is_waiting
                p.is_traveling=freight.is_traveling
                p.save()
            freight.save()
            return JsonResponse({'error': False})
        else:
            return freightIndex(request)


@login_required(login_url="login/")   
def freightTruck(request):
    if request.method == "POST":
        if request.is_ajax():
            freight = Freight.LogicFreight.get(id=request.POST['id'])
            temp= request.POST['truck']
            if temp == '-':
                truck = None
            else:
                truck = Truck.LogicTruck.get(id=temp)
            freight.truck = truck

            freight.save()
            return JsonResponse({'error': False})
        else:
            return freightIndex(request)
