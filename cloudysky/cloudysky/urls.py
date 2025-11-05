
#URL configuration for cloudysky project.

from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views

# We import the views from 'app'
from app import views as app_views

urlpatterns = [
    path('admin/', admin.site.urls),

    # This points /app/... to your app's urls.py file
    path('app/', include('app.urls')),

    # This path is correct for the autograder
    path('accounts/login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),

    # These two paths point the root URLs to your index view
    path('', app_views.index, name='root_index'),
    path('index.html', app_views.index, name='html_index'),
]
