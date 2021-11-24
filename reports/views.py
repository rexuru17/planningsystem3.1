from django.shortcuts import render
import pandas as pd
from sales.models import *
from products.models import *
from .forms import *

# Create your views here.
def reports_home(request):
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
        sales_df = pd.DataFrame(data)
        sales_df = sales_df.to_html()


    context = {
        'form':form,
        'sales_df':sales_df
    }
    return render(request, 'reports/reports.html', context)