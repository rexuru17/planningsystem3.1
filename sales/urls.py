"""planningsystem URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from os import name
from django.contrib import admin
from django.urls import path
from .views import *

app_name = 'sales'
urlpatterns = [
    path('customer/new/', CustomerCreateView.as_view(), name="customer-create"),
    path('customer/list/', CustomerListView.as_view(), name="customer-list"),
    path('customer/update/<int:pk>/', CustomerUpdateView.as_view(), name="customer-update"),
    path('customer/detail/<int:pk>/', CustomerDetailView.as_view(), name="customer-detail"),
    path('customer/delete/<int:pk>/', CustomerDeleteView.as_view(), name="customer-delete"),

    path('sales-channel/new/', SalesChannelCreateView.as_view(), name="saleschannel-create"),
    path('sales-channel/list/', SalesChannelListView.as_view(), name="saleschannel-list"),
    path('sales-channel/update/<int:pk>/', SalesChannelUpdateView.as_view(), name="saleschannel-update"),
    path('sales-channel/detail/<int:pk>/', SalesChannelDetailView.as_view(), name="saleschannel-detail"),
    path('sales-channel/delete/<int:pk>/', SalesChannelDeleteView.as_view(), name="saleschannel-delete"),

    path('plan-type/new/', PlanTypeCreateView.as_view(), name="plan-type-create"),
    path('plan-type/list/', PlanTypeListView.as_view(), name="plan-type-list"),
    path('plan-type/update/<int:pk>/', PlanTypeUpdateView.as_view(), name="plan-type-update"),
    path('plan-type/detail/<int:pk>/', PlanTypeDetailView.as_view(), name="plan-type-detail"),
    path('plan-type/delete/<int:pk>/', PlanTypeDeleteView.as_view(), name="plan-type-delete"),

    path('customer-plan-type/new/', CustomerPlanTypeCreateView.as_view(), name="customer-plan-type-create"),
    path('customer-plan-type/list/', CustomerPlanTypeListView.as_view(), name="customer-plan-type-list"),
    path('customer-plan-type/update/<int:pk>/', CustomerPlanTypeUpdateView.as_view(), name="customer-plan-type-update"),
    path('customer-plan-type/detail/<int:pk>/', CustomerPlanTypeDetailView.as_view(), name="customer-plan-type-detail"),
    path('customer-plan-type/delete/<int:pk>/', CustomerPlanTypeDeleteView.as_view(), name="customer-plan-type-delete"),

    path('sales-plan/new/', SalesPlanCreateView.as_view(), name="salesplan-create"),
    path('sales-plan/list/', SalesPlanListView.as_view(), name="salesplan-list"),
    path('sales-plan/update/<int:pk>/', SalesPlanUpdateView.as_view(), name="salesplan-update"),
    path('sales-plan/detail/<int:pk>/', SalesPlanDetailView.as_view(), name="salesplan-detail"),
    path('sales-plan/delete/<int:pk>/', SalesPlanDeleteView.as_view(), name="salesplan-delete"),

    path('plan-item/new/', PlanItemCreateView.as_view(), name="planitem-create"),
    path('plan-item/list/', PlanItemListView.as_view(), name="planitem-list"),
    path('plan-item/update/<int:pk>/', PlanItemUpdateView.as_view(), name="planitem-update"),
    path('plan-item/detail/<int:pk>/', PlanItemDetailView.as_view(), name="planitem-detail"),
    path('plan-item/delete/<int:pk>/', PlanItemDeleteView.as_view(), name="planitem-delete"),

    path('records/<int:pk>/', sales_records_lookup, name='sales-records-lookup'),
    path('plan/lookup/<int:pk>/', sales_plans_lookup, name='sales-plan-lookup'),

    path('upload-data/', upload_data_view, name='upload-data'),
    path('assign/<int:pk>/', assign_plan_types, name='plan-types-assign'),
    path('create/<int:pk>/', create_sales_plans, name='create-sales-plans'),
    path('generate_plan_items/<int:pk>/', generate_plan_items, name='generate-plan-items')

]
