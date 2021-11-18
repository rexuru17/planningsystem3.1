from django.db import models
from products.models import *
from django.db.models import Sum, Avg, Max, Min, constraints
from django.urls import reverse
import calendar
import datetime



# Create your models here.
class SalesChannel(models.Model):
    code = models.CharField(max_length=5, primary_key=True, unique=True)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
    

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['code', 'name'], name='%(app_label)s_%(class)s_is_unique'),

        ]

    def get_absolute_url(self):
        return reverse('sales:saleschannel-detail', kwargs={'pk': self.pk})


class Customer(models.Model):
    code = models.CharField(max_length=6, primary_key=True, unique=True)
    name = models.CharField(max_length=100)
    sales_channel = models.ForeignKey(SalesChannel, on_delete=models.CASCADE)
    portfolio = models.ManyToManyField(Product, blank=True, through='CustomerPortfolio')
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    include_in_channel_planning = models.BooleanField(default=False)
    

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['code', 'name'], name='%(app_label)s_%(class)s_is_unique'),

        ]

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('sales:customer-detail', kwargs={'pk': self.pk})

class CustomerPortfolio(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    added = models.DateField(blank=True, null=True)

    def __str__(self):
        return str(self.customer) + ' - ' + str(self.product)

    
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['customer', 'product'], name='%(app_label)s_%(class)s_is_unique'),

        ]

class PlanType(models.Model):
    
    def year_choices():
        return [(r,r) for r in range(datetime.date.today().year-2, datetime.date.today().year+10)]

    def current_year():
        return datetime.date.today().year

    PLAN_CHOICES = (
        ("FORECAST", "Forecast"),
        ("BUDGET", "Budget")
        )
    name = models.CharField(max_length=50, choices=PLAN_CHOICES, default="FORECAST", verbose_name='Plan Type')
    year = models.IntegerField(choices=year_choices(), default=current_year)


    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['name', 'year'], name='%(app_label)s_%(class)s_is_unique'),
        ]
    
    def __str__(self):
        info = str(self.name) + ' - ' + str(self.year)
        return str(info)
    
    def get_absolute_url(self):
        return reverse('sales:plan-type-detail', kwargs={'pk': self.pk})


class CustomerPlanType(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    plan_type = models.ForeignKey(PlanType, on_delete=models.CASCADE)
    
    def __str__(self):
        return str(self.plan_type.year) + ' ' + str(self.plan_type.name) + ' - ' +  str(self.customer.sales_channel) + ' - ' + str(self.customer)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['customer', 'plan_type'], name='%(app_label)s_%(class)s_is_unique'),
        ]
    

    def get_absolute_url(self):
        return reverse('sales:customer-plan-type-detail', kwargs={'pk': self.pk})

class SalesPlan(models.Model):
    cpt = models.ForeignKey(CustomerPlanType, on_delete=models.CASCADE, verbose_name="Customer Plan")
    period = models.DateField(blank=True, null=True)

    
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['period', 'cpt'], name='%(app_label)s_%(class)s_is_unique'),
        ]
           

    def __str__(self):
        if self.cpt.plan_type.name == "BUDGET":
            info = str(self.cpt) + ' - ' + str(self.period.strftime('%B'))
        elif self.cpt.plan_type.name == "FORECAST":
            info = str(self.cpt) + ' - ' + str(self.period.strftime('%B')) + ' - Week ' + str(self.period.isocalendar().week)
        else:
            pass
        return str(info)

    def get_absolute_url(self):
        return reverse('sales:salesplan-detail', kwargs={'pk': self.pk})

class PlanItem(models.Model):
    sales_plan = models.ForeignKey(SalesPlan, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['sales_plan', 'product'], name='%(app_label)s_%(class)s_is_unique'),

        ]

    @property
    def previous_qty(self):
        period = self.sales_plan.period
        year = self.sales_plan.cpt.plan_type.year
        customer = self.sales_plan.cpt.customer
        sales_channel = customer.sales_channel
        if sales_channel.customer_set.filter(include_in_channel_planning=True).count() == 1:
            if self.sales_plan.cpt.plan_type.name == "BUDGET":
                records = SalesRecords.objects.filter(customer__sales_channel=self.sales_plan.cpt.customer.sales_channel, product=self.product, date__month=period.month, date__year__range=((year-3), (year-1))).aggregate(Sum('quantity'))
            elif self.sales_plan.cpt.plan_type.name == "FORECAST":
                records = SalesRecords.objects.filter(customer__sales_channel=self.sales_plan.cpt.customer.sales_channel, product=self.product, date__week=period.isocalendar().week, date__year__range=((year-3), (year-1))).aggregate(Sum('quantity'))
        else:    
            if self.sales_plan.cpt.plan_type.name == "BUDGET":
                records = SalesRecords.objects.filter(customer=self.sales_plan.cpt.customer, product=self.product, date__month=period.month, date__year__range=((year-3), (year-1))).aggregate(Sum('quantity'))
            elif self.sales_plan.cpt.plan_type.name == "FORECAST":
                records = SalesRecords.objects.filter(customer=self.sales_plan.cpt.customer, product=self.product, date__week=period.isocalendar().week, date__year__range=((year-3), (year-1))).aggregate(Sum('quantity'))
        if records['quantity__sum']:
            return('{:.2f}'.format(float(records['quantity__sum']/3)))
        else:
            return 0

    def __str__(self):
        info = str(self.sales_plan) + ' - ' + str(self.product)
        return str(info)
    
    def get_absolute_url(self):
        return reverse('sales:planitem-detail', kwargs={'pk': self.pk})


class SalesRecords(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    date = models.DateField()
    quantity = models.FloatField()


    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['customer', 'product', 'date', 'quantity'], name='%(app_label)s_%(class)s_is_unique'),

        ]

    class Meta:
        verbose_name_plural = "Sales Records"

    def __str__(self):
        sales_records_info = str(self.customer) + ' - ' + str(self.date) + ' - ' + str(self.product)
        return str(sales_records_info)

class UploadData(models.Model):
    file_name = models.FileField(upload_to='tmp_data')
    uploaded = models.DateTimeField(auto_now=True)
    activated = models.BooleanField(default=False)

    def __str__(self):
        return f"File id: {self.id}"
