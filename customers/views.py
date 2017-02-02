from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.core.urlresolvers import reverse
from bson import json_util
import json
from dal import autocomplete
from django.contrib.auth.models import User
from .forms import *
from .models import *
from packages.models import *
from django.core.paginator import Paginator



class CustomerAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        if not self.request.user.is_authenticated():
            return Customer.LogicCustomer.none()

        qs = Customer.LogicCustomer.all()

        if self.q:
            qs1 = qs.filter(name__icontains=self.q)
            qs2 = qs.filter(rut__icontains=self.q)
            qs = qs1 | qs2
        return qs


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

