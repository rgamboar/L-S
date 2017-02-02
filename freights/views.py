from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from .forms import *
from .models import *
from django.core.paginator import Paginator
from bson import json_util
import json

import cStringIO as StringIO
from xhtml2pdf import pisa
from django.template.loader import get_template
from django.template import Context
from cgi import escape

from packages.models import *


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
def freightProfile(request, freight_id):
    freight = Freight.LogicFreight.get(id=freight_id)
    if freight.is_waiting:
        return freightProfileWaiting(request, freight)
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
def freightProfileWaiting(request, freight):
    own_packages = Package.LogicPackage.filter(freight=freight)
    packages = Package.LogicPackage.filter(start=freight.start, is_waiting= True, freight=None)
    search = 'All'
    if request.method == 'POST':
        form = IndexFreightForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            bfinal = data['bfinal']
            save = data
            save['bfinal'] = str(save['bfinal'])
            search = str(save['bfinal'])
            request.session['freightIndex']= save
            if (bfinal and bfinal != 'None'): 
                warehouse = Warehouse.LogicWarehouse.get(name=bfinal)
                packages = packages.filter(finish=warehouse)
            paginator = Paginator(packages, 25)
            num_page = 1
            packages = paginator.page(num_page)

    else:
        form = IndexFreightForm()
        if 'freightIndex' in request.session:
            data = request.session['freightIndex']
            num_page = request.GET.get('page')
            if request.GET.__contains__('page'):
                bfinal = data['bfinal']
                search = bfinal
                success=True
                if (bfinal and bfinal != 'None'): 
                    warehouse = Warehouse.LogicWarehouse.get(name=bfinal)
                    packages = packages.filter(finish=warehouse)
            else:
                num_page = 1
        else:
            num_page = 1
        paginator = Paginator(packages, 25)
        packages = paginator.page(num_page)
    if search == 'None':
        search = 'All'
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
            'form': form,
            'search' : search,

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

@login_required(login_url="login/")
def freightLoad(request):
    if request.method == "POST":
        if request.is_ajax():
            freight = Freight.LogicFreight.get(id=request.POST['id'])
            packages = Package.LogicPackage.filter(start=freight.start, is_waiting= True, freight=None)
            name= request.POST['finish']
            if not name == 'All':
                warehouse = Warehouse.LogicWarehouse.get(name=name)
                packages = packages.filter(finish=warehouse)

            for package in packages:
                package.freight = freight
                package.save()

            return JsonResponse({'error': False})

