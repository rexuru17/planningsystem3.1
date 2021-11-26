from django.http.response import HttpResponse
from django.shortcuts import render
import pandas as pd
from sales.models import *
from products.models import *
from .forms import *

# Create your views here.
def reports_home(request):
    """
    This view downloads sales plans to csv file
    """
    form = SalesPlanSearchForm(request.POST or None)
    sales_df = None
    plan_type = None
    date_from = None
    date_to = None

    if request.method == "POST":
        plan_type = request.POST.get('plan_type')
        date_from = request.POST.get('date_from')
        date_to = request.POST.get('date_to')
        data = PlanItem.objects.filter(sales_plan__cpt__plan_type__name=plan_type,
        sales_plan__period_start__gte=date_from,
        sales_plan__period_start__lte=date_to,
        )
        sales_df = pd.DataFrame(data.values('sales_plan__cpt__plan_type__name', 
                                            'sales_plan__period_start__year',
                                            'sales_plan__period_start__month',
                                            'sales_plan__period_start', 
                                            'sales_plan__period_end',
                                            'sales_plan__cpt__customer__sales_channel__name', 
                                            'sales_plan__cpt__customer__code',
                                            'sales_plan__cpt__customer__name', 
                                            'product__product_subgroup__product_group__name', 
                                            'product__product_subgroup__name',  
                                            'product__code', 
                                            'product__name', 
                                            'quantity', 
                                            ))
        sales_df.rename({'sales_plan__cpt__plan_type__name': 'Plan', 
                        'sales_plan__cpt__customer__code': 'Customer Code', 
                        'sales_plan__cpt__customer__name': 'Customer Name', 
                        'sales_plan__cpt__customer__sales_channel__name': 'Sales Channel', 
                        'product__code': 'Product Code', 
                        'product__name': 'Product Name', 
                        'product__product_subgroup__name': 'Product SubGroup', 
                        'product__product_subgroup__product_group__name': 'Product Group', 
                        'quantity': "Quantity", 
                        'sales_plan__period_start': 'Period From', 
                        'sales_plan__period_end': 'Period To', 
                        'sales_plan__period_start__month': 'Month',
                        'sales_plan__period_start__year': 'Year',
                        }, axis=1, inplace=True)
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = f"attachment; filename={plan_type} - {date_from[0:4]} - All Customers.csv"
        sales_df.to_csv(path_or_buf=response, index=False)
        return response
    context = {
        'form':form,
        'sales_df':sales_df
    }
    return render(request, 'reports/reports.html', context)