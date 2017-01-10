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
            if form.startAddress:
                is_waiting=False
                is_transmitter=True
            if form.finishAddress:
                is_reciever=True
            form.save()
            return HttpResponseRedirect('/')
    else:
        form = PackageForm()
    return render(request, 'intranet/packages/create.html', {'form': form})





@login_required(login_url="login/")
def packageIndex(request, traveling=False, finish=False, delivered=False, transmitter=False):
    if traveling:
        packages = Package.objects.filter(is_traveling=True)
        page = "traveling"
    elif finish:
        packages= Package.objects.filter(is_waiting=False, is_traveling=False, is_delivered=False)
        page = "finish"
    elif transmitter:
        packages= Package.objects.filter(is_waiting=False, is_traveling=False, is_delivered=False, is_transmitter=True)
        page = "finish"
    elif delivered:
        packages= Package.objects.filter(is_waiting=False, is_traveling=False, is_delivered=True)
        page = "delivered"
    else:
        packages = Package.objects.filter(is_waiting=True)
        for i in packages:
            i.posibleFreight= Freight.objects.filter(start=i.start, finish= i.finish, is_waiting= True)
            if i.freight:
                i.posibleFreight = i.posibleFreight.exclude(id= i.freight.id)
        page = "inicio"

    return render(request, 'intranet/packages/index.html', 
        {
            'packages': packages,
            'page': page,
        })

@login_required(login_url="login/")
def packageProfile(request, package_id, load=False):
    if load:
        if request.method == 'POST':
            form = DriverForm(request.POST)
            if form.is_valid():
                form.save()
                return HttpResponseRedirect('/')
        else:
            package = Package.objects.get(id=package_id)
            own_packages = Package.objects.filter(package=package)
            packages = Package.objects.filter(start=package.start, finish= package.finish, is_waiting= True)
            packages = packages.exclude(package=package_id)

        return render(request, 'intranet/packages/profile.html', 
            {
                'package': package,
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
            package = Package.objects.get(id=package_id)

        return render(request, 'intranet/packages/profile.html', 
            {
                'package': package,
                'send' : True,
            })

@login_required(login_url="login/")   
def packageFreight(request):
    if request.method == "POST":
        if request.is_ajax():
            package = Package.objects.get(id=request.POST['id'])
            if package.is_waiting== False:
                return JsonResponse({'error': True})
            temp= request.POST['freight']
            if temp == '-':
                freight = None
            else:
                freight = Freight.objects.get(id=temp)
                if freight.is_waiting== False:
                    return JsonResponse({'error': True})
            package.freight = freight

            package.save()
            return JsonResponse({'error': False})
        else:
            return packageIndex(request)


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
def freightIndex(request, traveling=False, finish=False):
    if traveling:
        freights = Freight.objects.filter(is_traveling=True)
        page = "traveling"
    elif finish:
        freights= Freight.objects.filter(is_waiting=False, is_traveling=False)
        page = "finish"
    else:
        freights= Freight.objects.filter(is_waiting=True)
        for freight in freights:
            freight.posibleDriver= Driver.objects.all().exclude(id=freight.driver.id)
            freight.posibleTruck= Truck.objects.all().exclude(id=freight.truck.id)
        page = "inicio"

    return render(request, 'intranet/freights/index.html', 
        {
            'freights': freights,
            'page': page,
        })

@login_required(login_url="login/")
def freightProfile(request, freight_id, load=False):
    freight = Freight.objects.get(id=freight_id)
    if freight.is_waiting:
        return freightProfileWaiting(request, freight, load)
    elif freight.is_traveling:
        return freightProfileTraveling(request, freight)
    else:
        return freightProfileFinish(request, freight)


@login_required(login_url="login/")
def freightProfileFinish(request, freight):
    own_packages = Package.objects.filter(freight=freight)
    return render(request, 'intranet/freights/profileFinish.html', 
        {
            'freight': freight,
            'own_packages' : own_packages,
        })

@login_required(login_url="login/")
def freightProfileTraveling(request, freight):
    own_packages = Package.objects.filter(freight=freight)
    return render(request, 'intranet/freights/profileTraveling.html', 
        {
            'freight': freight,
            'own_packages' : own_packages,
        })


@login_required(login_url="login/")
def freightProfileWaiting(request, freight, load):
    if load:
        own_packages = Package.objects.filter(freight=freight)
        packages = Package.objects.filter(start=freight.start, finish= freight.finish, is_waiting= True)
        packages = packages.exclude(freight=freight)
        
        freight.posibleDriver= Driver.objects.all().exclude(id=freight.driver.id)
        freight.posibleTruck= Truck.objects.all().exclude(id=freight.truck.id)
        print (freight)
        return render(request, 'intranet/freights/profile.html', 
            {
                'freight': freight,
                'packages' : packages,
                'own_packages' : own_packages,

            })
    else:
        own_packages = Package.objects.filter(freight=freight)
        freight.posibleDriver= Driver.objects.all().exclude(id=freight.driver.id)
        freight.posibleTruck= Truck.objects.all().exclude(id=freight.truck.id)
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
            freight = Freight.objects.get(id=request.POST['id'])
            temp= request.POST['driver']
            if temp == '-':
                driver = None
            else:
                driver = Driver.objects.get(id=temp)
            freight.driver = driver

            freight.save()
            return JsonResponse({'error': False})
        else:
            return freightIndex(request)

@login_required(login_url="login/")   
def freightState(request):
    if request.method == "POST":
        if request.is_ajax():
            freight = Freight.objects.get(id=request.POST['id'])
            temp= request.POST['state']
            if temp == 'traveling':
                freight.is_traveling = True
                freight.is_waiting = False
                print("1")
            elif temp == 'finish':
                freight.is_traveling= False
                freight.is_waiting= False
                print("2")
            packages = Package.objects.filter(freight=freight)
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
            freight = Freight.objects.get(id=request.POST['id'])
            temp= request.POST['truck']
            if temp == '-':
                truck = None
            else:
                truck = Truck.objects.get(id=temp)
            freight.truck = truck

            freight.save()
            return JsonResponse({'error': False})
        else:
            return freightIndex(request)
