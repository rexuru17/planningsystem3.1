from django.shortcuts import render
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from products.models import *
from django.urls import reverse_lazy

######### PRODUCT VIEWS ##############

class ProductCreateView(CreateView):
    model = Product
    fields = '__all__'
    success_url = reverse_lazy('products:list-product')


class ProductListView(ListView):
    model = Product
    ordering = ['product_subgroup', 'code', 'weight']


class ProductUpdateView(UpdateView):
    model = Product
    fields = '__all__'
    success_url = reverse_lazy('products:list-product')


class ProductDetailView(DetailView):
    model = Product


class ProductDeleteView(DeleteView):
    model = Product
    success_url = reverse_lazy('products:list-product')

######### PRODUCT GROUP VIEWS ##############

class ProductGroupCreateView(CreateView):
    model = ProductGroup
    fields = '__all__'
    success_url = reverse_lazy('products:list-product-group')


class ProductGroupListView(ListView):
    model = ProductGroup
    ordering = ['name',]


class ProductGroupUpdateView(UpdateView):
    model = ProductGroup
    fields = '__all__'
    success_url = reverse_lazy('products:list-product-group')


class ProductGroupDetailView(DetailView):
    model = ProductGroup


class ProductGroupDeleteView(DeleteView):
    model = ProductGroup
    success_url = reverse_lazy('products:list-product-group')

######### PRODUCT SUBGROUP VIEWS ##############

class ProductSubGroupCreateView(CreateView):
    model = ProductSubGroup
    fields = '__all__'
    success_url = reverse_lazy('products:list-product-subgroup')


class ProductSubGroupListView(ListView):
    model = ProductSubGroup
    ordering = ['product_group', 'name']


class ProductSubGroupUpdateView(UpdateView):
    model = ProductSubGroup
    fields = '__all__'
    success_url = reverse_lazy('products:list-product-subgroup')


class ProductSubGroupDetailView(DetailView):
    model = ProductSubGroup


class ProductSubGroupDeleteView(DeleteView):
    model = ProductSubGroup
    success_url = reverse_lazy('products:list-product-subgroup')
