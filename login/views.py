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
from dal import autocomplete


import cStringIO as StringIO
from xhtml2pdf import pisa
from django.template.loader import get_template
from django.template import Context
from django.http import HttpResponse
from cgi import escape


class CustomerAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        # Don't forget to filter out results depending on the visitor !
        if not self.request.user.is_authenticated():
            return Customer.LogicCustomer.none()

        qs = Customer.LogicCustomer.all()

        if self.q:
            qs = qs.filter(name__icontains=self.q)

        return qs


def render_to_pdf(template_src, context_dict):
    template = get_template(template_src)
    context = Context(context_dict)
    html  = template.render(context)
    result = StringIO.StringIO()

    pdf = pisa.pisaDocument(StringIO.StringIO(html.encode("ISO-8859-1")), result)
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    return HttpResponse('We had some errors<pre>%s</pre>' % escape(html))

def freightPdf(request, freight_id=1):
    freight = Freight.LogicFreight.get(id=freight_id)
    packages = Package.LogicPackage.filter(freight=freight)

    return render_to_pdf(
            'freightPdf.html',
            {
                'pagesize':'A4',
                'packages': packages,
                'freight': freight,
                'date': datetime.now(),
            }
        )

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
def package(request):
    success=False
    customerCheck= False
    if request.method == 'POST':
        form = PackageForm(request.POST, prefix="f")
        provider=  FastCustomerForm(request.POST,prefix="p")
        consignee= FastCustomerForm(request.POST,prefix="c")
        if form.is_valid():
            data = form.cleaned_data
            if data['provider'] and data['consignee']:
                obj = form.save(commit=False)
                if obj.payer:
                    obj.customer=obj.provider
                else:
                    obj.customer=obj.consignee
                if obj.startAddress:
                    obj.is_waiting=True
                    obj.is_transmitter=True
                if obj.finishAddress:
                    obj.is_reciever=True
                obj.creator = request.user
                obj.save()
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
                    if obj.startAddress:
                        obj.is_waiting=True
                        obj.is_transmitter=True
                    if obj.finishAddress:
                        obj.is_reciever=True
                    obj.creator = request.user
                    obj.save()
                    success=True
                else:
                    customerCheck=True
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
                    if obj.startAddress:
                        obj.is_waiting=True
                        obj.is_transmitter=True
                    if obj.finishAddress:
                        obj.is_reciever=True
                    obj.creator = request.user
                    obj.save()
                    success=True
                else:
                    customerCheck=True
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
                    if obj.startAddress:
                        obj.is_waiting=True
                        obj.is_transmitter=True
                    if obj.finishAddress:
                        obj.is_reciever=True
                    obj.creator = request.user
                    obj.save()
                    success=True
                else:
                    customerCheck=True
        oldForm= form
        form = PackageForm(initial={
            'start': oldForm.cleaned_data['start'],
            'startAddress': oldForm.cleaned_data['startAddress'],
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
        'customerCheck': customerCheck
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
        packages= Package.LogicPackage.filter(is_waiting=False, is_traveling=False, is_delivered=False, is_transmitter=False)
    elif status == "4":
        packages = Package.LogicPackage.filter(is_delivered=True)
    else:
        packages = Package.LogicPackage.all()
    if rate:
        packages= packages.filter(rate='0')
    if (binicial and binicial != 'None'):
        print(binicial)
        warehouse = Warehouse.LogicWarehouse.get(name=binicial)
        packages = packages.filter(start=warehouse)
    if (bfinal and bfinal != 'None'): 
        print(bfinal)
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
        packages_pay = packages.filter(pay__icontains=search)
        packages = packages_client | packages_risk | packages_volume | packages_quantity | packages_weight | packages_chance | packages_rate | packages_pay
    return packages

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
    


@login_required(login_url="login/")
def packageIndex(request, traveling=False, finish=False, delivered=False):
    if traveling:
        packages = Package.LogicPackage.filter(is_traveling=True)
        page = "traveling"
    elif finish:
        packages= Package.LogicPackage.filter(is_waiting=False, is_traveling=False, is_delivered=False, is_transmitter=False)
        page = "finish"
    elif delivered:
        packages= Package.LogicPackage.filter(is_waiting=False, is_traveling=False, is_delivered=True)
        page = "delivered"
    else:
        packages = Package.LogicPackage.filter(is_waiting=True)
        page = "inicio"
    num_page = request.GET.get('page', 1)
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
def packageProfileTransmitter(request, package):
    return render(request, 'intranet/packages/profileTransmitter.html', 
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
            if temp == 'transmitter':
                package.is_waiting = True
                package.transmitter= request.user
                package.transmitDate = datetime.now()
            elif temp == 'delivered':
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
def customerUpdate(request, customer_id):
    customer = Customer.LogicCustomer.get(id=customer_id)
    form = CustomerFormUpdate(request.POST or None, instance=customer)
    if form.is_valid():
          form.save()
          return customerProfile(request, customer_id)
    return render(request, 'intranet/customers/update.html', 
        {
            'form': form,
            'customer_id': customer_id,
        })
    

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
def customerSearch(request):
    success= False
    if request.method == 'POST':
        form = SearchCustomerForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            rut = data['rut']
            name = data['name']
            phone = data['phone']
            repEmail = data['repEmail']
            save = data
            request.session['customerSearch']= save

            success=True

            customers = customerFilter(request, rut, name, phone, repEmail)

            paginator = Paginator(customers, 25)

            num_page = 1
            
            page = paginator.page(num_page)
            
            customers = page

            return render(request, 'intranet/customers/search.html', {
                'form': form,
                'success': success,
                'customers': customers,
            })
    else:
        form = SearchCustomerForm()
        if 'customerSearch' in request.session:
            data = request.session['customerSearch']
            num_page = request.GET.get('page')
            if num_page:
                rut = data['rut']
                name = data['name']
                phone = data['phone']
                repEmail = data['repEmail']
                success=True
                customers = customerFilter(request, rut, name, phone, repEmail)
                paginator = Paginator(customers, 25)
                page = paginator.page(num_page)
                customers = page
                return render(request, 'intranet/customers/search.html', {
                    'form': form,
                    'success': success,
                    'customers': customers,
                })

    return render(request, 'intranet/customers/search.html', {
        'form': form,
    })

@login_required(login_url="login/")
def customerFilter(request, rut, name, phone, repEmail):
    customer = Customer.LogicCustomer.all()
    if rut:
        customer = customer.filter(rut__icontains=rut)
    if name:
        customer = customer.filter(name__icontains=name)
    if phone:
        customer = customer.filter(phone__icontains=phone)
    if repEmail:
        customer = customer.filter(repEmail__icontains=repEmail)
    return customer



@login_required(login_url="login/")
def customerIndex(request):

    customers = Customer.LogicCustomer.filter()
    num_page = request.GET.get('page', 1)
    paginator = Paginator(customers, 25)
    customers = paginator.page(num_page)
    return render(request, 'intranet/customers/index.html', 
        {
            'customers': customers,
        })

@login_required(login_url="login/")
def customerProfile(request, customer_id):
    customer = Customer.LogicCustomer.get(id=customer_id)
    own_packages = Package.LogicPackage.filter(customer=customer)
    num_page = request.GET.get('page', 1)
    paginator = Paginator(own_packages, 25)
    own_packages = paginator.page(num_page)
    return render(request, 'intranet/customers/profile.html', 
        {
            'customer': customer,
            'own_packages' : own_packages,
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
        page = "inicio"

    num_page = request.GET.get('page', 1)
    paginator = Paginator(freights, 25)
    freights = paginator.page(num_page)
    if page == "inicio":
        for freight in freights:
            freight.posibleDriver = Driver.LogicDriver.all()
            freight.posibleTruck= Truck.LogicTruck.all()
            if freight.driver:
                freight.posibleDriver = freight.posibleDriver.exclude(id=freight.driver.id)
            if freight.truck:
                freight.posibleTruck= freight.posibleTruck.exclude(id=freight.truck.id)


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
                freight.sender= request.user
                freight.sendDate = datetime.now()
            elif temp == 'finish':
                freight.is_traveling= False
                freight.is_waiting= False
                freight.receiver= request.user
                freight.receiveDate = datetime.now()
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



@login_required(login_url="login/")
def freightSearch(request):
    success= False
    if request.method == 'POST':
        form = SearchFreightForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            startDate = data['startDate']
            finishDate = data['finishDate']
            status = data['status']
            binicial = data['binicial']
            bfinal = data['bfinal']
            save = data
            save['startDate']= json.dumps(save['startDate'], default=json_util.default)
            save['finishDate']= json.dumps(save['finishDate'], default=json_util.default)
            save['binicial'] = str(save['binicial'])
            save['bfinal'] = str(save['bfinal'])
            request.session['freightSearch']= save

            success=True

            freights = freightsFilter(request,startDate, finishDate, status, binicial, bfinal)

            paginator = Paginator(freights, 25)

            num_page = 1
            
            page = paginator.page(num_page)
            
            freights = page

            return render(request, 'intranet/freights/search.html', {
                'form': form,
                'success': success,
                'freights': freights,
            })
    else:
        form = SearchFreightForm()
        if 'freightSearch' in request.session:
            data = request.session['freightSearch']
            num_page = request.GET.get('page')
            if num_page:
                startDate = json.loads(data['startDate'], object_hook=json_util.object_hook)
                finishDate = json.loads(data['finishDate'], object_hook=json_util.object_hook)
                status = data['status']
                binicial = data['binicial']
                bfinal = data['bfinal']
                success=True
                freights = freightsFilter(request,startDate, finishDate, status, binicial, bfinal)
                paginator = Paginator(freights, 25)
                page = paginator.page(num_page)
                freights = page
                return render(request, 'intranet/freights/search.html', {
                    'form': form,
                    'success': success,
                    'freights': freights,
                })

    return render(request, 'intranet/freights/search.html', {
        'form': form,
    })



@login_required(login_url="login/")
def freightsFilter(request, start, finish, status, binicial, bfinal):
    if status == "1":
        freights = Freight.LogicFreight.filter(is_waiting=True)
    elif status == "2":
        freights = Freight.LogicFreight.filter(is_traveling=True)
    elif status == "3":
        freights= Freight.LogicFreight.filter(is_waiting=False, is_traveling=False)
    else:
        freights = Freight.LogicFreight.all()
    if (binicial and binicial != 'None'):
        warehouse = Warehouse.LogicWarehouse.get(name=binicial)
        freights = freights.filter(start=warehouse)
    if (bfinal and bfinal != 'None'):
        warehouse = Warehouse.LogicWarehouse.get(name=bfinal)
        freights = freights.filter(finish=warehouse)
    if start:
        freights = freights.filter(createDate__gte=start)
    if finish:
        freights = freights.filter(createDate__lte=finish)
    return freights
