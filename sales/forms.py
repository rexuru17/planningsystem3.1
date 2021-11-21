from django import forms
from django.db.models import fields
from django.forms import widgets
from django.forms.formsets import formset_factory
from .models import *


class UploadDataForm(forms.ModelForm):
    class Meta:
        model = UploadData
        fields = ('file_name',)

class SalesPlanForm(forms.ModelForm):
    class Meta:
        model = SalesPlan
        fields = '__all__'
        widgets = {
            'period_start': forms.DateInput(attrs={'type': 'date'}),
            'period_end': forms.DateInput(attrs={'type': 'date'}),
        }

"""
THIS CLASS SHOULD WORK FOR PREFILLED PRODUCTS
"""
class PlanItemForm(forms.ModelForm):
    previous_qty = forms.CharField(widget = forms.TextInput(attrs={'readonly':'readonly'}))
    display_product = forms.CharField(widget = forms.TextInput(attrs={'readonly':'readonly', 'size':'50'}))
    class Meta:
        model = PlanItem
        fields = '__all__'
        widgets = {
            'product': forms.HiddenInput(),
            'sales_plan': forms.HiddenInput(),
        }
    field_order = ['sales_plan', 'product','display_product', 'quantity', 'previous_qty']


class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = '__all__'
        widgets = {
            
        }

class PlanTypeForm(forms.ModelForm):
    class Meta:
        model = PlanType
        fields = '__all__'
        widgets = {
            
        }



class CustomerPlanTypeForm(forms.ModelForm):
    class Meta:
        model = CustomerPlanType
        fields = '__all__'
        widgets = {
            'customer': forms.HiddenInput()
        }