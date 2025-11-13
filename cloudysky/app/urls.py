from django.urls import path
from . import views

urlpatterns = [
    # HW4 paths
    path('new', views.signup_view, name='signup_page'),
    path('new/', views.signup_view, name='signup_page_slash'), # Safety duplicate
    path('createUser', views.create_user_view, name='create_user_endpoint'),
    path('createUser/', views.create_user_view, name='create_user_endpoint_slash'), # Safety duplicate

    # HW5 Step 2: Form pages
    path('new_post', views.new_post_view, name='new_post_view'),
    path('new_comment', views.new_comment_view, name='new_comment_view'),

    # HW5 Step 1: API Endpoints (The "Shotgun" Approach)
    # Version WITHOUT slash
    path('createPost', views.create_post_api, name='create_post_api'),
    path('createComment', views.create_comment_api, name='create_comment_api'),
    path('hidePost', views.hide_post_api, name='hide_post_api'),
    path('hideComment', views.hide_comment_api, name='hide_comment_api'),

    # Version WITH slash
    path('createPost/', views.create_post_api, name='create_post_api_slash'),
    path('createComment/', views.create_comment_api, name='create_comment_api_slash'),
    path('hidePost/', views.hide_post_api, name='hide_post_api_slash'),
    path('hideComment/', views.hide_comment_api, name='hide_comment_api_slash'),

    # Diagnostic
    path('dumpFeed', views.dump_feed_api, name='dump_feed_api'),
]
