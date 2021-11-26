from django.db.models import Sum, Avg, Max, Min
from django.db.models.functions import TruncMonth, TruncYear
import csv
import pandas as pd
from sales.models import *
from products.models import *

def create_products():
    file_path = 'products.csv'
    df = pd.read_csv(file_path)
    pgroups = []
    pgs = ProductGroup.objects.all()
    df1 = df.groupby(['prod_sub_group', 'prod_group']).size()
    for index, row in df1.iteritems():
        x = ProductSubGroup(
            name=index[0],
            product_group=pgs.get(name=index[1])
        )
        if x not in pgroups:
            pgroups.append(x)
    ProductSubGroup.objects.bulk_create(pgroups)
    subgroups = ProductSubGroup.objects.all()
    products = []
    for index, row in df.iterrows():
        products.append(Product(
            product_subgroup = subgroups.get(name=row['prod_sub_group']),
            code = row['itemcode'],
            name = row['itemname'],
            unit_of_measure = row['UoM'],
            weight = row['weight'],
            weight_text = row['weight_txt'],
        ))
    Product.objects.bulk_create(products)
    return print('upload complete')



def upload_records(file_path):
    """
    this function should be able to take in a csv file (properly formatted), then read it into a dataframe and save to database
    for now, it is set up to read sales_records.csv mock data with cca 330k lines. Upload time cca 2min.
    """
    file_path = 'channels.csv'
    df = pd.read_csv(file_path) # Create a view that takes in a csv file and puts it into this function
    channels = []
    for index, row in df.iterrows():
        channels.append(SalesChannel(
            code=row['sales_channel_code'],
            name = row['sales_channel']
        ))
    SalesChannel.objects.bulk_create(channels)
    file_path = 'customers.csv'
    df = pd.read_csv(file_path)
    customers = []
    channels = SalesChannel.objects.all()
    for index, row in df.iterrows():
        customers.append(Customer(
            code = row['customer_code'],
            name = row['customer_name'],
            sales_channel = channels.get(code=row['sales_channel_code']),
        ))
    Customer.objects.bulk_create(customers)
    
    file_path = 'sales_records.csv'
    df = pd.read_csv(file_path)
    sales_records = []
    products = Product.objects.all()
    customers = Customer.objects.all()
    for index, row in df.iterrows():
        sales_records.append(SalesRecords(
            customer=customers.get(code=row['customer_code']), 
            product=products.get(code=row['itemcode']), 
            date=row['date'], 
            quantity=row['quantity'])
            )
    
    SalesRecords.objects.bulk_create(sales_records)
    return print('upload complete')


def get_sales_records():
    """
    this function should be able to take in a customer or a certain period and spit out some sort of pivoted data regarding sales records
    for now, it displays all sales records by product.
    """
    sales_records = Product.objects.annotate(Sum('salesrecords__quantity')).annotate(year=TruncYear('salesrecords__date')).values('year')
    df = pd.DataFrame(sales_records.values())
    df_pivot = df.pivot_table(index=['code', 'name'], columns='year', values='salesrecords__quantity__sum', aggfunc=sum)

    # filtering months and years, but this gives average per sales instance, not per month.
    sales_records = Product.objects.filter(salesrecords__date__month=6, salesrecords__date__year__range=('2017', '2020')).annotate(Avg('salesrecords__quantity'))
    
    # this does not work!!!
    sales_records = Product.objects.filter(salesrecords__date__year__range=('2017', '2020')).annotate(Avg(Sum('salesrecords__quantity'))).annotate(month=TruncMonth('salesrecords__date'))


"""
Utility to automatically create budget plans based on sales records and projected budget growth goals, based on product, product group, etc

This function creates sales plan of type BUDGET, for every month, based on average sales of previous x years (X will be a choice by user)
Then for each customer and month, based on client input, for each product it creates quantity 
(average of X years for a month with function to increase/decrease qquantity)

"""
def create_sales_plans(customer_id):
    customer = Customer.objects.get(code=customer_id)
    portfolio = customer.portfolio.all()
    plan_type = PlanType.objects.get(name='BUDGET', year='2021')
    budget_items = []
    salesplans = []
    for x in range(1,13):
        salesplans.append(SalesPlan(customer=customer, period=x, plan_type=plan_type))
    SalesPlan.objects.bulk_create(salesplans)
    salesplans = SalesPlan.objects.filter(customer=customer)
    for salesplan in salesplans:
        for item in portfolio:
            budget_items.append(PlanItem(sales_plan=SalesPlan.objects.get(id=salesplan.id), product=item, quantity=PlanItem(sales_plan=salesplan, product=item).previous_qty))
    PlanItem.objects.bulk_create(budget_items)



"""
This function generates FC plans according to budget plans, and budget plans according to 3 year previous average sales quantity
"""
def generate_plan_items(sales_plan):
    sales_plan = sales_plan
    customer = sales_plan.cpt.customer
    portfolio = customer.portfolio.all()
    initial = []
    for item in portfolio:
        if sales_plan.cpt.plan_type.name == "FORECAST":
            quantity = PlanItem(sales_plan=sales_plan, product=item).get_budget_qty
        else:
            quantity = PlanItem(sales_plan=sales_plan, product=item).previous_qty
        initial.append(PlanItem(sales_plan=sales_plan,
                                product=item,
                                quantity=quantity,
                                ))
    PlanItem.objects.bulk_create(initial)