from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views

# --- ADD THIS IMPORT ---
from app import views as app_views

urlpatterns = [
    path('admin/', admin.site.urls),

    path('app/', include('app.urls')),


    path('accounts/login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),

   
    path('', app_views.index, name='root_index'),
    path('index.html', app_views.index, name='html_index'),
]
