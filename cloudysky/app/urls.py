from django.urls import path
from . import views

urlpatterns = [
    # --- HW 7 / GRADER ENDPOINTS ---
    
    # 1. Hide Post (Slash and No Slash)
    path('hidePost/', views.hide_post, name='hide_post'),
    path('hidePost', views.hide_post, name='hide_post_no_slash'),
    
    # 2. Hide Comment (Slash and No Slash)
    path('hideComment/', views.hide_comment, name='hide_comment'),
    path('hideComment', views.hide_comment, name='hide_comment_no_slash'),

    # 3. Dump Feed (Slash and No Slash)
    # This is the critical HW7 endpoint
    path('dumpFeed/', views.dump_feed, name='dump_feed'),
    path('dumpFeed', views.dump_feed, name='dump_feed_no_slash'),


    # --- HW 6 / FRONTEND PATHS ---
    path('feed/', views.feed, name='feed'),
    path('post/<int:post_id>/', views.post_detail, name='post_detail'),
    path('feed-page/', views.feed_page, name='feed_page'),
    path('post-page/<int:post_id>/', views.post_page, name='post_page'),


    # --- HW 4 & 5 / LEGACY PATHS ---
    path('new', views.signup_view, name='signup_page'),
    path('new/', views.signup_view, name='signup_page_slash'),
    path('createUser', views.create_user_view, name='create_user_endpoint'),
    path('createUser/', views.create_user_view, name='create_user_endpoint_slash'),

    # HW5 Step 2: Form pages
    path('new_post', views.new_post_view, name='new_post_view'),
    path('new_comment', views.new_comment_view, name='new_comment_view'),

    # HW5 Step 1: API Endpoints
    path('createPost', views.create_post_api, name='create_post_api'),
    path('createComment', views.create_comment_api, name='create_comment_api'),
    path('createPost/', views.create_post_api, name='create_post_api_slash'),
    path('createComment/', views.create_comment_api, name='create_comment_api_slash'),
]