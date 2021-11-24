from django import forms
from django.forms.forms import Form
from sales.models import *


types = tuple(PlanType.objects.all().values_list('name', 'name').distinct())



class SalesPlanSearchForm(forms.Form):
    date_from = forms.DateField(widget=forms.DateInput(attrs={'type':'date'}))
    date_to = forms.DateField(widget=forms.DateInput(attrs={'type':'date'}))
    plan_type = forms.ChoiceField(choices=types)