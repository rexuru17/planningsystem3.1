from django.urls import path
from .views import *

app_name = 'reports'
urlpatterns = [
    path('', reports_home, name='reports')
]