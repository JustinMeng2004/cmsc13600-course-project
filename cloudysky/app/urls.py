from django.urls import path
from . import views

urlpatterns = [
    # HW 6 Paths
    	# Matches 'app/feed'
    path('feed/', views.feed, name='feed'),
    
    	# Matches 'app/post/1', 'app/post/45', etc.
    path('post/<int:post_id>/', views.post_detail, name='post_detail'),

    	# ... your api urls ...
    path('feed-page/', views.feed_page, name='feed_page'),
    path('post-page/<int:post_id>/', views.post_page, name='post_page'),


	# --- NEW ENDPOINTS FOR GRADER ---
    # 1. Catch /hidePost/ (with slash)
    path('hidePost/', views.hide_post, name='hide_post'),
    # 2. Catch /hidePost (no slash) - Pointing to the NEW view
    path('hidePost', views.hide_post, name='hide_post_no_slash'),
    
    # 3. Same for Comments
    path('hideComment/', views.hide_comment, name='hide_comment'),
    path('hideComment', views.hide_comment, name='hide_comment_no_slash'),

    # 4. Dump Feed
    path('dumpFeed/', views.dump_feed, name='dump_feed'),
    path('dumpFeed', views.dump_feed, name='dump_feed_no_slash'),


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
    # path('hidePost', views.hide_post_api, name='hide_post_api'),
    # path('hideComment', views.hide_comment_api, name='hide_comment_api'),

    # Version WITH slash
    path('createPost/', views.create_post_api, name='create_post_api_slash'),
    path('createComment/', views.create_comment_api, name='create_comment_api_slash'),
    # path('hidePost/', views.hide_post_api, name='hide_post_api_slash'),
    # path('hideComment/', views.hide_comment_api, name='hide_comment_api_slash'),

    # Diagnostic
    path('dumpFeed', views.dump_feed_api, name='dump_feed_api'),
]
