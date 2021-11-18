from django.contrib import admin
from .models import *


# Register your models here.
admin.site.register(Customer)
admin.site.register(SalesChannel)
admin.site.register(SalesPlan)
admin.site.register(PlanItem)
admin.site.register(SalesRecords)
admin.site.register(UploadData)
admin.site.register(PlanType)
admin.site.register(CustomerPlanType)
admin.site.register(CustomerPortfolio)