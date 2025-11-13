# app/urls.py

from django.urls import path
from . import views

urlpatterns = [
    # --- HW4 Paths (already here) ---
    path('new', views.signup_view, name='signup_page'),
    path('createUser', views.create_user_view, name='create_user_endpoint'),

    # --- HW5 Step 2: Form-serving pages ---
    path('new_post', views.new_post_view, name='new_post_view'),
    path('new_comment', views.new_comment_view, name='new_comment_view'),

    # --- HW5 Step 1: API endpoints ---
    path('createPost/', views.create_post_api, name='create_post_api'),
    path('createComment/', views.create_comment_api, name='create_comment_api'),
    path('hidePost/', views.hide_post_api, name='hide_post_api'),
    path('hideComment/', views.hide_comment_api, name='hide_comment_api'),

    # --- HW5 Step 3: Diagnostic endpoint ---
    path('dumpFeed', views.dump_feed_api, name='dump_feed_api'),
]
