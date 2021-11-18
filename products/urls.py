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
from django.contrib import admin
from django.urls import path
from . import views as product_views


app_name = 'products'
urlpatterns = [
    path('group/create/', product_views.ProductGroupCreateView.as_view(), name='create-product-group'),
    path('group/list/', product_views.ProductGroupListView.as_view(), name='list-product-group'),
    path('group/update/<int:pk>/', product_views.ProductGroupUpdateView.as_view(), name='update-product-group'),
    path('group/delete/<int:pk>/', product_views.ProductGroupDeleteView.as_view(), name='delete-product-group'),
    path('group/detail/<int:pk>/', product_views.ProductGroupDetailView.as_view(), name='detail-product-group'),
    
    path('group/subgroup/create/', product_views.ProductSubGroupCreateView.as_view(), name='create-product-subgroup'),
    path('group/subgroup/list/', product_views.ProductSubGroupListView.as_view(), name='list-product-subgroup'),
    path('group/subgroup/update/<int:pk>/', product_views.ProductSubGroupUpdateView.as_view(), name='update-product-subgroup'),
    path('group/subgroup/delete/<int:pk>/', product_views.ProductSubGroupDeleteView.as_view(), name='delete-product-subgroup'),
    path('group/subgroup/detail/<int:pk>/', product_views.ProductSubGroupDetailView.as_view(), name='detail-product-subgroup'),
    
    path('create/', product_views.ProductCreateView.as_view(), name='create-product'),
    path('list/', product_views.ProductListView.as_view(), name='list-product'),
    path('update/<int:pk>/', product_views.ProductUpdateView.as_view(), name='update-product'),
    path('delete/<int:pk>/', product_views.ProductDeleteView.as_view(), name='delete-product'),
    path('detail/<int:pk>/', product_views.ProductDetailView.as_view(), name='detail-product'),

]
