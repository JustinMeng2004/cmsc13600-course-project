# app/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('time', views.get_current_time, name='time'),
    path('sum', views.calculate_sum, name='sum'),
]
