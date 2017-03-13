from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from .forms import *
from .models import *
from django.core.paginator import Paginator
import cStringIO as StringIO
from xhtml2pdf import pisa
from django.template.loader import get_template
from django.template import Context
from cgi import escape
from bson import json_util
import json

from customers.forms import *
from freights.forms import *
from customers.models import *


def render_to_pdf(template_src, context_dict):
    template = get_template(template_src)
    context = Context(context_dict)
    html  = template.render(context)
    result = StringIO.StringIO()

    pdf = pisa.pisaDocument(StringIO.StringIO(html.encode("ISO-8859-1")), result)
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    return HttpResponse('We had some errors<pre>%s</pre>' % escape(html))


def packagePdf(request, package_id=1):
    package = Package.LogicPackage.get(id=package_id)

    return render_to_pdf(
            'packagePdf.html',
            {
                'pagesize':'A4',
                'package': package,
                'date': datetime.now(),
            }
        )

@login_required(login_url="login/")
def package(request):
    package=False
    success=False
    customerCheck= False
    makeProvider= False
    makeConsignee= False
    rutProvider = False
    rutConsignee = False
    if request.method == 'POST':
        form = PackageForm(request.POST, prefix="f")
        provider=  FastCustomerForm(request.POST,prefix="p")
        consignee= FastCustomerForm(request.POST,prefix="c")

        if form.is_valid():
            data = form.cleaned_data
            if not data['provider']:
                makeProvider = True
            if not data['consignee']:
                makeConsignee = True
            if data['provider'] and data['consignee']:
                obj = form.save(commit=False)
                if obj.payer == "Proveedor":
                    obj.customer=obj.provider
                elif obj.payer == "Consignatario":
                    obj.customer=obj.consignee
                else:
                    obj.customer = None
                if obj.finishAddress:
                    obj.is_reciever=True
                obj.creator = request.user
                obj.save()
                package = obj
                success=True
            elif data['provider']:
                if consignee.is_valid() and not Customer.objects.filter(rut=consignee.cleaned_data['rut']):
                    data= consignee.cleaned_data
                    consigneeInstance = Customer(name=data['name'] ,rut=data['rut'], address=data['address'], phone=data['phone'], repEmail=data['repEmail'], creator_id= request.user.id)
                    consigneeInstance.save()
                    obj = form.save(commit=False)
                    obj.consignee=consigneeInstance
                    if obj.payer:
                        obj.customer=obj.provider
                    else:
                        obj.customer=obj.consignee
                    if obj.finishAddress:
                        obj.is_reciever=True
                    obj.creator = request.user
                    obj.save()
                    package = obj
                    success=True
                else:
                    customerCheck=True
                    if Customer.objects.filter(rut=consignee.cleaned_data['rut']):
                        rutConsignee = True                    
            elif data['consignee']:
                if provider.is_valid() and not Customer.objects.filter(rut=provider.cleaned_data['rut']):
                    data= provider.cleaned_data
                    providerInstance = Customer(name=data['name'] ,rut=data['rut'], address=data['address'], phone=data['phone'], repEmail=data['repEmail'], creator_id= request.user.id)
                    providerInstance.save()
                    obj = form.save(commit=False)
                    obj.provider=providerInstance
                    if obj.payer:
                        obj.customer=obj.provider
                    else:
                        obj.customer=obj.consignee
                    if obj.finishAddress:
                        obj.is_reciever=True
                    obj.creator = request.user
                    obj.save()
                    package = obj
                    success=True
                else:
                    customerCheck=True
                    if Customer.objects.filter(rut=provider.cleaned_data['rut']):
                        rutProvider = True
            else:
                if provider.is_valid() and consignee.is_valid() and not Customer.objects.filter(rut=provider.cleaned_data['rut']) and not Customer.objects.filter(rut=consignee.cleaned_data['rut']):
                    data= provider.cleaned_data
                    providerInstance = Customer(name=data['name'] ,rut=data['rut'], address=data['address'], phone=data['phone'], repEmail=data['repEmail'], creator_id= request.user.id)
                    data= consignee.cleaned_data
                    consigneeInstance = Customer(name=data['name'] ,rut=data['rut'], address=data['address'], phone=data['phone'], repEmail=data['repEmail'], creator_id= request.user.id)
                    providerInstance.save()
                    consigneeInstance.save()
                    obj = form.save(commit=False)
                    obj.provider=providerInstance
                    obj.consignee=consigneeInstance                    
                    if obj.payer:
                        obj.customer=obj.provider
                    else:
                        obj.customer=obj.consignee
                    if obj.finishAddress:
                        obj.is_reciever=True
                    obj.creator = request.user
                    obj.save()
                    package = obj
                    success=True
                else:
                    customerCheck=True
                    if Customer.objects.filter(rut=provider.cleaned_data['rut']):
                        rutProvider = True
                    if Customer.objects.filter(rut=consignee.cleaned_data['rut']):
                        rutConsignee = True 
        oldForm= form
        form = PackageForm(initial={
            'start': oldForm.cleaned_data['start'],
            'finish': oldForm.cleaned_data['finish'],
            'finishAddress': oldForm.cleaned_data['finishAddress'],
            'provider': oldForm.cleaned_data['provider'],
            'consignee': oldForm.cleaned_data['consignee'],
            }, prefix="f")
    else:
        form = PackageForm(prefix="f")
        provider=  FastCustomerForm(prefix="p")
        consignee= FastCustomerForm(prefix="c")
    return render(request, 'intranet/packages/create.html', {
        'form': form,
        'success': success,
        'provider': provider,
        'consignee': consignee,
        'customerCheck': customerCheck,
        'makeProvider': makeProvider,
        'makeConsignee': makeConsignee,
        'rutProvider': rutProvider,
        'rutConsignee': rutConsignee,
        'package': package
    })


@login_required(login_url="login/")
def packageSearch(request):
    success= False
    if request.method == 'POST':
        form = SearchBoxForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            startDate = data['startDate']
            finishDate = data['finishDate']
            search = data['search']
            status = data['status']
            binicial = data['binicial']
            bfinal = data['bfinal']
            rate = data['rate']
            save = data
            save['startDate']= json.dumps(save['startDate'], default=json_util.default)
            save['finishDate']= json.dumps(save['finishDate'], default=json_util.default)
            save['binicial'] = str(save['binicial'])
            save['bfinal'] = str(save['bfinal'])
            request.session['packageSearch']= save

            success=True

            packages = packagesFilter(request,startDate, finishDate, search, status, binicial, bfinal, rate)

            paginator = Paginator(packages, 25)

            num_page = 1
            
            page = paginator.page(num_page)
            
            packages = page

            return render(request, 'intranet/packages/search.html', {
                'form': form,
                'success': success,
                'packages': packages,
            })
    else:
        form = SearchBoxForm()
        if 'packageSearch' in request.session:
            data = request.session['packageSearch']
            num_page = request.GET.get('page')
            if num_page:
                startDate = json.loads(data['startDate'], object_hook=json_util.object_hook)
                finishDate = json.loads(data['finishDate'], object_hook=json_util.object_hook)
                search = data['search']
                status = data['status']
                binicial = data['binicial']
                bfinal = data['bfinal']
                success=True
                packages = packagesFilter(request,startDate, finishDate, search, status, binicial, bfinal)
                paginator = Paginator(packages, 25)
                page = paginator.page(num_page)
                packages = page
                return render(request, 'intranet/packages/search.html', {
                    'form': form,
                    'success': success,
                    'packages': packages,
                })

    return render(request, 'intranet/packages/search.html', {
        'form': form,
    })



@login_required(login_url="login/")
def packagesFilter(request, start, finish, search, status, binicial, bfinal, rate):
    if status == "1":
        packages = Package.LogicPackage.filter(is_waiting=True)
    elif status == "2":
        packages = Package.LogicPackage.filter(is_traveling=True)
    elif status == "3":
        packages= Package.LogicPackage.filter(is_waiting=False, is_traveling=False, is_delivered=False)
    elif status == "4":
        packages = Package.LogicPackage.filter(is_delivered=True)
    else:
        packages = Package.LogicPackage.all()
    if rate:
        packages= packages.filter(rate='0')
    if (binicial and binicial != 'None'):
        warehouse = Warehouse.LogicWarehouse.get(name=binicial)
        packages = packages.filter(start=warehouse)
    if (bfinal and bfinal != 'None'): 
        warehouse = Warehouse.LogicWarehouse.get(name=bfinal)
        packages = packages.filter(finish=warehouse)
    if start:
        packages = packages.filter(createDate__gte=start)
    if finish:
        packages = packages.filter(createDate__lte=finish)
    if search:
        packages_client = packages.filter(customer__name__icontains=search)
        packages_risk = packages.filter(risk__icontains=search)
        packages_volume = packages.filter(volume__icontains=search)
        packages_quantity = packages.filter(quantity__icontains=search)
        packages_weight = packages.filter(weight__icontains=search)
        packages_chance = packages.filter(chance__icontains=search)
        packages_rate = packages.filter(rate__icontains=search)
        packages = packages_client | packages_risk | packages_volume | packages_quantity | packages_weight | packages_chance | packages_rate
    return packages



@login_required(login_url="login/")
def packageIndex(request, traveling=False, finish=False, delivered=False):
    if traveling:
        packages = Package.LogicPackage.filter(is_traveling=True)
        page = "traveling"
    elif finish:
        packages= Package.LogicPackage.filter(is_waiting=False, is_traveling=False, is_delivered=False)
        page = "finish"
    elif delivered:
        packages= Package.LogicPackage.filter(is_waiting=False, is_traveling=False, is_delivered=True)
        page = "delivered"
    else:
        packages = Package.LogicPackage.filter(is_waiting=True)
        page = "inicio"
    if request.method == 'POST':
        form = IndexPackageForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            binicial = data['binicial']
            bfinal = data['bfinal']
            save = data
            save['binicial'] = str(save['binicial'])
            save['bfinal'] = str(save['bfinal'])
            request.session['packageIndex']= save
            if (binicial and binicial != 'None'):
                warehouse = Warehouse.LogicWarehouse.get(name=binicial)
                packages = packages.filter(start=warehouse)
            if (bfinal and bfinal != 'None'): 
                warehouse = Warehouse.LogicWarehouse.get(name=bfinal)
                packages = packages.filter(finish=warehouse)
            paginator = Paginator(packages, 25)
            num_page = 1
            packages = paginator.page(num_page)

    else:
        form = IndexPackageForm()
        if 'packageIndex' in request.session:
            data = request.session['packageIndex']
            num_page = request.GET.get('page')
            if request.GET.__contains__('page'):
                binicial = data['binicial']
                bfinal = data['bfinal']
                success=True
                if (binicial and binicial != 'None'):
                    warehouse = Warehouse.LogicWarehouse.get(name=binicial)
                    packages = packages.filter(start=warehouse)
                if (bfinal and bfinal != 'None'): 
                    warehouse = Warehouse.LogicWarehouse.get(name=bfinal)
                    packages = packages.filter(finish=warehouse)
            else:
                num_page = 1
        else:
            num_page = 1
        paginator = Paginator(packages, 25)
        packages = paginator.page(num_page)

    if page == "inicio":
        for i in packages:
            i.posibleFreight= Freight.LogicFreight.filter(start=i.start, finish= i.finish, is_waiting= True)
            if i.freight:
                i.posibleFreight = i.posibleFreight.exclude(id= i.freight.id)

    return render(request, 'intranet/packages/index.html', 
        {
            'packages': packages,
            'page': page,
            'form': form,
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
    elif package.is_receiver:
        return packageProfileReceiver(request, package)
    else:
        return packageProfileFinish(request, package)


@login_required(login_url="login/")
def packageProfileFinish(request, package):
    return render(request, 'intranet/packages/profileFinish.html', 
        {
            'package': package,
        })

@login_required(login_url="login/")
def packageProfileReceiver(request, package):
    return render(request, 'intranet/packages/profileReceiver.html', 
        {
            'package': package,
        })


@login_required(login_url="login/")
def packageProfileDelivered(request, package):
    return render(request, 'intranet/packages/profileDelivered.html', 
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
    package.posibleFreight= Freight.LogicFreight.filter(start=package.start, finish= package.finish, is_waiting= True)
    if package.freight:
        package.posibleFreight = package.posibleFreight.exclude(id= package.freight.id)
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
def packageState(request):
    if request.method == "POST":
        if request.is_ajax():
            package = Package.LogicPackage.get(id=request.POST['id'])
            temp= request.POST['state']
            if temp == 'delivered':
                package.is_delivered = True
                package.deliverer= request.user
                package.deliverDate = datetime.now()
            package.save()
            return JsonResponse({'error': False})
        else:
            return freightIndex(request)

@login_required(login_url="login/")   
def packageRate(request):
    if request.method == "POST":
        if request.is_ajax():
            package = Package.LogicPackage.get(id=request.POST['id'])
            rate= request.POST['rate']
            if rate> 0:
                package.rate= rate
                package.save()
            return JsonResponse({'error': False})
        else:
            return freightIndex(request)


@login_required(login_url="login/")   
def pickup(request):
    success=False
    pickup=False
    if request.method == 'POST':
        form = PickUpForm(request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.creator = request.user
            obj.save()
            success=True
            pickup=obj
            form = PickUpForm(initial={
                'warehouse': form.cleaned_data['warehouse'],
                'address': form.cleaned_data['address'],
                'customer': form.cleaned_data['customer'],
                'truck': form.cleaned_data['truck'],
                'driver': form.cleaned_data['driver'],
                })
    else:
        form = PickUpForm()
    return render(request, 'intranet/pickups/create.html', {
        'form': form,
        'success': success,
        'pickup': pickup
    })



@login_required(login_url="login/")   
def pickupWaiting(request):
    pickups = PickUp.LogicPickUp.filter(is_waiting=True)

    num_page = request.GET.get('page', 1)
    paginator = Paginator(pickups, 25)
    pickups = paginator.page(num_page)

    return render(request, 'intranet/pickups/index.html', 
        {
            'pickups': pickups,
        })




@login_required(login_url="login/")   
def pickupReady(request):
    pickups = PickUp.LogicPickUp.filter(is_waiting=False)

    num_page = request.GET.get('page', 1)
    paginator = Paginator(pickups, 25)
    pickups = paginator.page(num_page)

    return render(request, 'intranet/pickups/index.html', 
        {
            'pickups': pickups,
            'ready': True,
        })



@login_required(login_url="login/")   
def pickupProfile(request, pickup_id):
    pickup = PickUp.LogicPickUp.get(id=pickup_id)
    return render(request, 'intranet/pickups/profile.html', 
        {
            'pickup': pickup,
        })


@login_required(login_url="login/")   
def pickupPackage(request):
    if request.method == "POST":
        if request.is_ajax():
            package = Package.LogicPackage.get(id=request.POST['package_id'])
            pickup = PickUp.LogicPickUp.get(id=request.POST['pickup_id'])
            pickup.package = package
            pickup.deliverer = request.user
            pickup.is_waiting = False
            pickup.pickUpDate = datetime.now()
            pickup.save()
            return JsonResponse({'error': False})
        else:
            return freightIndex(request)