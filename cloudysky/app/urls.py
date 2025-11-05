# app/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('time', views.get_current_time, name='time'),
    path('sum', views.calculate_sum, name='sum'),
    path('', views.index, name='index'),
    path('new/', views.signup_view, name='signup_page'),
    path('createUser', views.create_user_view, name='create_user_endpoint'),
]
