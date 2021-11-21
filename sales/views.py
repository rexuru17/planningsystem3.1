from django.http.response import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from numpy import product
from products.models import *
from sales.models import *
from sales.forms import *
from django.urls import reverse_lazy
from django.forms import formset_factory
from sales.filters import *
from sales.utils import upload_records
import pandas as pd
import datetime
import calendar
# Create your views here.


########### Upload Data Views ######################
def upload_data_view(request):
    form = UploadDataForm(request.POST or None, request.FILES or None)
    
    if form.is_valid():
        form.save()
        form = UploadDataForm()
        obj = UploadData.objects.get(activated=False)
        file_path = obj.file_name.path
        upload_records(file_path=file_path)
        obj.activated = True
        obj.save()
    context = {
        'form': form,
    }
    return render(request, 'sales/upload.html', context)


########### Sales Channel Views ######################


class SalesChannelCreateView(CreateView):
    model = SalesChannel
    fields = '__all__'


class SalesChannelDetailView(DetailView):
    model = SalesChannel
    

class SalesChannelListView(ListView):
    model = SalesChannel


class SalesChannelUpdateView(UpdateView):
    model = SalesChannel
    fields = '__all__'
    success_url = reverse_lazy('sales:saleschannel-list')
    
    
class SalesChannelDeleteView(DeleteView):
    model = SalesChannel
    success_url = reverse_lazy('sales:saleschannel-list')



########### Customer Views ######################


class CustomerCreateView(CreateView):
    model = Customer
    form_class = CustomerForm


class CustomerDetailView(DetailView):
    model = Customer
    

class CustomerListView(ListView):
    model = Customer
    ordering = ['sales_channel', 'code',]


class CustomerUpdateView(UpdateView):
    model = Customer
    fields = '__all__'
    success_url = reverse_lazy('sales:customer-list')
    
    
class CustomerDeleteView(DeleteView):
    model = Customer
    success_url = reverse_lazy('sales:customer-list')


########### Sales Plan Type Views ######################


class PlanTypeCreateView(CreateView):
    model = PlanType
    form_class = PlanTypeForm
  
  
class PlanTypeDetailView(DetailView):
    model = PlanType
    

class PlanTypeListView(ListView):
    model = PlanType


class PlanTypeUpdateView(UpdateView):
    model = PlanType
    fields = '__all__'
    success_url = reverse_lazy('sales:plan-type-list')
    
    
class PlanTypeDeleteView(DeleteView):
    model = PlanType
    success_url = reverse_lazy('sales:plan-type-list')


########### Customer Plan Type Views ######################


class CustomerPlanTypeCreateView(CreateView):
    model = CustomerPlanType
    form_class = CustomerPlanTypeForm
  
  
class CustomerPlanTypeDetailView(DetailView):
    model = CustomerPlanType
    

class CustomerPlanTypeListView(ListView):
    model = CustomerPlanType


class CustomerPlanTypeUpdateView(UpdateView):
    model = CustomerPlanType
    fields = '__all__'
    success_url = reverse_lazy('sales:customer-plan-type-list')
    
    
class CustomerPlanTypeDeleteView(DeleteView):
    model = CustomerPlanType
    success_url = reverse_lazy('sales:customer-plan-type-list')


########### Sales Plan Views ######################


class SalesPlanCreateView(CreateView):
    model = SalesPlan
    form_class = SalesPlanForm


class SalesPlanDetailView(DetailView):
    model = SalesPlan
    

class SalesPlanListView(ListView):
    model = SalesPlan
    paginate_by = 100



class SalesPlanUpdateView(UpdateView):
    model = SalesPlan
    fields = '__all__'
    success_url = reverse_lazy('sales:salesplan-list')
    
    
class SalesPlanDeleteView(DeleteView):
    model = SalesPlan
    success_url = reverse_lazy('sales:salesplan-list')


########### Plan - Item Views ######################


class PlanItemCreateView(CreateView):
    model = PlanItem
    # form_class = PlanItemForm # USE THIS FOR PREFILLED FORMSETS!!!
    fields = '__all__'

class PlanItemDetailView(DetailView):
    model = PlanItem
    

class PlanItemListView(ListView):
    model = PlanItem
    paginate_by = 100


class PlanItemUpdateView(UpdateView):
    model = PlanItem
    fields = '__all__'
    success_url = reverse_lazy('sales:planitem-list')
    
    
class PlanItemDeleteView(DeleteView):
    model = PlanItem
    success_url = reverse_lazy('sales:planitem-list')


########### Sales Data Lookup Views ######################

"""
Work on filtering data correctly for customers
"""
def sales_records_lookup(request, pk):
    customer = Customer.objects.get(code=pk)
    sales_records = customer.salesrecords_set.all()
    myFilter = SalesRecordsFilter(request.GET, queryset=sales_records)
    sales_records = myFilter.qs

    context = {
        'customer': customer,
        'sales_records': sales_records,
        'myFilter': myFilter,
    }
    return render(request, 'sales/salesrecords_lookup.html', context)

def sales_plans_lookup(request, pk):
    customer = Customer.objects.get(code=pk)
    plans = customer.salesplan_set.all()
    myFilter = SalesPlanFilter(request.GET, queryset=plans)
    plans = myFilter.qs
    x = plans.values('planitem__product__code', 'planitem__product__name', 'planitem__quantity', 'customer__name', 'plan_type__name', 'period_start')
    df = pd.DataFrame(x)
    pivot = df.pivot_table(index=['planitem__product__code', 'planitem__product__name'], columns=['period_start'], values='planitem__quantity', aggfunc=sum)
    context = {
        'customer': customer,
        'plans': plans,
        'myFilter': myFilter,
        'data': pivot.to_html()
    }
    return render(request, 'sales/salesplan_lookup.html', context)


############## CUSTOM VIEWS ##############

def assign_plan_types(request, pk):
    customer = get_object_or_404(Customer, code=pk)
    if customer.include_in_channel_planning == False:
        return HttpResponse(f"Customer {customer} is not included in sales planning. Press back button to return")
        # CREATE A COOLER RESPONSE
    plantypes = PlanType.objects.all()
    initial = []
    for plan in plantypes:
        initial.append({'customer':customer, 'plan_type':plan})
    PlanTypeFormSet = formset_factory(CustomerPlanTypeForm, extra=0)
    formset = PlanTypeFormSet(initial=initial)
    if request.method == "POST":
        formset = PlanTypeFormSet(request.POST)
        for form in formset:
            if form.is_valid():
                form.save()
        return redirect('sales:customer-detail', pk=pk)
    context = {
        'formset': formset,
        'customer': customer
    }
    return render(request, 'sales/assign_plan_types.html', context)

def create_sales_plans(request, pk):
    cpt = get_object_or_404(CustomerPlanType, id=pk)
    initial = []
    form = SalesPlanForm()
    if cpt.plan_type.name == "BUDGET":
        for month in range(1, 13):
            initial.append({
                'cpt': cpt,
                'period_start': datetime.date(cpt.plan_type.year, month, 1),
                'period_end': datetime.date(cpt.plan_type.year, month, calendar.monthrange(cpt.plan_type.year, month)[1]),

            })
    elif cpt.plan_type.name == "FORECAST":
        month = datetime.date.today().month + 1
        weeks = len(calendar.monthcalendar(cpt.plan_type.year, month))
        day = 1
        for week in range(1, weeks+1):
            if day in range(1, calendar.monthrange(cpt.plan_type.year, month)[1]+1):
                start_of_week = datetime.date(cpt.plan_type.year, month, day) - datetime.timedelta(days=datetime.date(cpt.plan_type.year, month, day).weekday())
                end_of_week = start_of_week + datetime.timedelta(days=6)
                if day == 1:
                    start_date = datetime.date(cpt.plan_type.year, month, day)
                else:
                    start_date = start_of_week
                if end_of_week.month == month:
                    end_date = end_of_week
                else:
                    end_date = datetime.date(cpt.plan_type.year, month, calendar.monthrange(cpt.plan_type.year, month)[1])
                if start_date.weekday() != 6:
                    initial.append({
                        'cpt':cpt,
                        'period_start': start_date,
                        'period_end': end_date,
                    
                    })
                else:
                    pass
            day = end_date.day + 1
    else:
        pass
    SalesPlanFormSet = formset_factory(SalesPlanForm, extra=0)
    formset = SalesPlanFormSet(initial=initial)
    if request.method == 'POST':
        formset = SalesPlanFormSet(request.POST)
        if formset.is_valid():
            for form in formset:
                form.save()
            return redirect('sales:salesplan-list')
    context = {
        'cpt':cpt,
        'formset':formset,
    }
    return render(request, 'sales/create_sales_plans.html', context)

def generate_plan_items(request, pk):
    sales_plan = get_object_or_404(SalesPlan, id=pk)
    period = sales_plan.period_start.strftime('%B')
    customer = sales_plan.cpt.customer
    portfolio = customer.portfolio.all()
    initial = []
    for item in portfolio:
        initial.append({
            'sales_plan': sales_plan,
            'product': item,
            'quantity': 0,
            'previous_qty': PlanItem(sales_plan=sales_plan, product=item).previous_qty,
            'display_product':Product.objects.get(code=item.code)
        })
    PlanItemFormset = formset_factory(PlanItemForm, extra=0)
    formset = PlanItemFormset(initial=initial)
    if request.method == "POST":
        formset = PlanItemFormset(request.POST)
        if formset.is_valid():
            for form in formset:
                # quantity = form.cleaned_data['quantity']
                form.save()
            return redirect('sales:planitem-list')
    context = {
        'formset':formset,
        'customer':customer,
        'sales_plan': sales_plan,
        'period': period,
    }
    return render(request, 'sales/create_planitems.html', context)