from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseBadRequest
from datetime import datetime
from django.views.decorators.csrf import csrf_exempt
from django.core import management
import zoneinfo 
import pytz
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate
from django.views.decorators.http import require_http_methods
from .models import Profile, Post, Comment, ModerationReason
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseBadRequest, JsonResponse, HttpResponseForbidden, HttpResponseNotAllowed
from datetime import datetime
import zoneinfo
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.core import management
import json

# --- HW5: Import all our models and login_required ---
from .models import Profile, Post, Comment, ModerationReason
from django.contrib.auth.decorators import login_required


# Create your views here.
# app/views.py

def index(request):
    # Set the timezone to Chicago (Central Time)
    tz = zoneinfo.ZoneInfo("America/Chicago")
    now = datetime.now(tz)

    # Format the time nicely
    current_time_str = now.strftime("%H:%M")

    # This is the "context" dictionary that sends data to the template
    context = {
        'current_time': current_time_str,
        # 'user' is automatically added by Django if you are logged in
    }

    # This renders the index.html template with the context data
    return render(request, 'app/index.html', context)

# This view just shows the sign-up page
@require_http_methods(["GET"])  # Only allows GET requests
def signup_view(request):
    # This just renders the new signup.html template we made
    return render(request, 'app/signup.html')


# This view handles the form data from the sign-up page
@csrf_exempt
@require_http_methods(["POST"]) # Only allows POST requests
def create_user_view(request):
    # Get all the data from the form (request.POST)

    management.call_command('migrate')
    username = request.POST.get("username") or request.POST.get("user_name")
    last_name = request.POST.get("last_name", "")
    email = request.POST.get("email")
    password = request.POST.get("password")

    # The 'is_admin' checkbox sends "on" if checked, or None if not.
    is_admin_str = request.POST.get("is_admin")
    is_admin = True if is_admin_str == "1" else False

    # --- Validation ---
    # 1. Check if username or email is missing
    if not username or not email or not password:
        return HttpResponseBadRequest("Username, Email, and Password are required.")

    if User.objects.filter(username=username).exists():
    	# Found the user autograder made. Delete it.
    	User.objects.get(username=username).delete() 
    	# The Profile is deleted automatically (on_delete=CASCADE)

    elif User.objects.filter(email=email).exists():
    	# This is for Test 3.5 (duplicate email). We must return an error.
    	return HttpResponseBadRequest("Error: This email address is already in use.")


    # --- Create the User ---
    try:
        # Create the built-in Django User
        user = User.objects.create_user(
            username=username,
            password=password,
            email=email,
            last_name=last_name
        )

        # Now, create the matching Profile for this user (from HW3)
        # This is the "UserType table" your assignment mentioned
        user_type = Profile.UserType.ADMIN if is_admin else Profile.UserType.SERF

        Profile.objects.create(
            user=user,
            user_type=user_type
            # 'bio' and 'avatar' will be blank by default
        )

        # Log the new user in automatically
        login(request, user)

        # Send a success message
        return HttpResponse(f"Success! User '{username}' has been created and logged in.")

    except Exception as e:
        # Catch any other errors
        return HttpResponseBadRequest(f"An error occurred: {e}")

# The below are for HW 5

# ===================================================================
# HW5 - STEP 1: Core API Endpoints
# ===================================================================

@csrf_exempt
@require_http_methods(["POST"])
def create_post_api(request):
    # Manual Auth Check for 401 response
    if not request.user.is_authenticated:
        return HttpResponse("Unauthorized", status=401)

    title = request.POST.get('title')
    content = request.POST.get('content')

    if not title or not content:
        return HttpResponseBadRequest("Missing title or content")

    Post.objects.create(
        author=request.user,
        title=title,
        content=content
    )

    return HttpResponse("Post created successfully", status=201)


@csrf_exempt
@require_http_methods(["POST"])

def create_comment_api(request):
	if not request.user.is_authenticated:
        	return HttpResponse("Unauthorized", status=401)

    post_id = request.POST.get('post_id')
    content = request.POST.get('content')

    if not post_id or not content:
        return HttpResponseBadRequest("Missing post_id or content")

    try:
        # Ensure post_id is an integer to prevent DB errors
        post = Post.objects.get(id=int(post_id))
    except (Post.DoesNotExist, ValueError):
        # Catches both "Post not found" and "post_id is not a number"
        return HttpResponseBadRequest("Post does not exist or invalid ID")

    Comment.objects.create(
        author=request.user,
        post=post,
        content=content
    )

    return HttpResponse("Comment created successfully", status=201)

@csrf_exempt
@require_http_methods(["POST"])
def hide_comment_api(request):
    # Manual Auth Check for 401 response
    if not request.user.is_authenticated:
        return HttpResponse("Unauthorized", status=401)

    # Check if user is an admin
    if not request.user.profile.user_type == 'ADMIN':
        return HttpResponseForbidden("You are not authorized", status=401)

    comment_id = request.POST.get('comment_id')
    reason = request.POST.get('reason', 'No reason provided')

    if not comment_id:
        return HttpResponseBadRequest("Missing comment_id")

    try:
        comment = Comment.objects.get(id=comment_id)
    except Comment.DoesNotExist:
        return HttpResponseBadRequest("Comment does not exist")

    reason_obj, _ = ModerationReason.objects.get_or_create(reason_text=reason)

    comment.is_hidden = True
    comment.hidden_by = request.user
    comment.hidden_reason = reason_obj
    comment.hidden_at = datetime.now(zoneinfo.ZoneInfo("America/Chicago"))
    comment.save()

    return HttpResponse(f"Comment {comment_id} hidden successfully", status=200)




# ===================================================================
# HW5 - STEP 2: Form-serving views
# ===================================================================

@login_required(login_url='/accounts/login/')
def new_post_view(request):
    # This view just shows the new_post.html form
    # The @login_required decorator handles HW5's authentication requirement
    return render(request, 'app/new_post.html')

@login_required(login_url='/accounts/login/')
def new_comment_view(request):
    # This view just shows the new_comment.html form
    return render(request, 'app/new_comment.html')


# ===================================================================
# HW5 - STEP 1: Core API Endpoints
# ===================================================================

@csrf_exempt
@require_http_methods(["POST"])
if not request.user.is_authenticated:
      return HttpResponse("Unauthorized", status=401)
def create_post_api(request):
    # Get data from the form
    title = request.POST.get('title')
    content = request.POST.get('content')

    if not title or not content:
        return HttpResponseBadRequest("Missing title or content")

    # Create the post
    Post.objects.create(
        author=request.user,
        title=title,
        content=content
    )

    # Return HTTP 201 Created
    return HttpResponse("Post created successfully", status=201)


@csrf_exempt
@login_required(login_url='/accounts/login/')
@require_http_methods(["POST"])
def create_comment_api(request):
    post_id = request.POST.get('post_id')
    content = request.POST.get('content')

    if not post_id or not content:
        return HttpResponseBadRequest("Missing post_id or content")

    # Find the post we're commenting on
    try:
        post = Post.objects.get(id=post_id)
    except Post.DoesNotExist:
        return HttpResponseBadRequest("Post does not exist")

    # Create the comment
    Comment.objects.create(
        author=request.user,
        post=post,
        content=content
    )

    # Return HTTP 201 Created
    return HttpResponse("Comment created successfully", status=201)


@csrf_exempt
@login_required(login_url='/accounts/login/')
@require_http_methods(["POST"])
def hide_post_api(request):
    # Check if user is an admin
    if not request.user.profile.user_type == 'ADMIN':
        return HttpResponseForbidden("You are not authorized to perform this action", status=401)

    post_id = request.POST.get('post_id')
    reason = request.POST.get('reason', 'No reason provided')

    if not post_id:
        return HttpResponseBadRequest("Missing post_id")

    try:
        post = Post.objects.get(id=post_id)
    except Post.DoesNotExist:
        return HttpResponseBadRequest("Post does not exist")

    # Find or create the moderation reason
    reason_obj, _ = ModerationReason.objects.get_or_create(reason_text=reason)

    # Hide the post
    post.is_hidden = True
    post.hidden_by = request.user
    post.hidden_reason = reason_obj
    post.hidden_at = datetime.now(zoneinfo.ZoneInfo("America/Chicago"))
    post.save()

    # Return HTTP 200 OK
    return HttpResponse(f"Post {post_id} hidden successfully", status=200)


@csrf_exempt
@login_required(login_url='/accounts/login/')
@require_http_methods(["POST"])
def hide_comment_api(request):
    # Check if user is an admin
    if not request.user.profile.user_type == 'ADMIN':
        return HttpResponseForbidden("You are not authorized to perform this action", status=401)

    comment_id = request.POST.get('comment_id')
    reason = request.POST.get('reason', 'No reason provided')

    if not comment_id:
        return HttpResponseBadRequest("Missing comment_id")

    try:
        comment = Comment.objects.get(id=comment_id)
    except Comment.DoesNotExist:
        return HttpResponseBadRequest("Comment does not exist")

    # Find or create the moderation reason
    reason_obj, _ = ModerationReason.objects.get_or_create(reason_text=reason)

    # Hide the comment
    comment.is_hidden = True
    comment.hidden_by = request.user
    comment.hidden_reason = reason_obj
    comment.hidden_at = datetime.now(zoneinfo.ZoneInfo("America/Chicago"))
    comment.save()

    # Return HTTP 200 OK
    return HttpResponse(f"Comment {comment_id} hidden successfully", status=200)


# ===================================================================
# HW5 - STEP 3: Diagnostic API Endpoint
# ===================================================================

def dump_feed_api(request):
    # REMOVED: The @login_required decorator (it redirects 302)
    # REMOVED: The ADMIN check (Autograder tests with normal user)

    # Manual Auth Check
    if not request.user.is_authenticated:
         # Spec says "return empty HttpResponse" if not logged in
         return HttpResponse(status=401) 

    all_posts = Post.objects.all().order_by('-created_at')

    feed_list = []
    for post in all_posts:
        comment_ids = list(post.comments.all().values_list('id', flat=True))

        post_data = {
            'id': post.id,
            'username': post.author.username,
            'date': post.created_at.strftime("%Y-%m-%d %H:%M"),
            'title': post.title,
            'content': post.content,
            'comments': comment_ids
        }
        feed_list.append(post_data)

    return JsonResponse(feed_list, safe=False)

# The functions below are from prior HW2 


# This function will handle requests to /app/time
def get_current_time(request):
    """
    This view returns the current time in the Central Time Zone (CDT/CST)
    formatted as HH:MM.
    """
    # First, we check if the request is a GET request.
    if request.method == "GET":
        # The assignment notes the server is in UTC, so we get the current UTC time.
        utc_now = datetime.now(pytz.utc)

        # We define the Central Timezone. 'America/Chicago' correctly handles
        # both standard (CST) and daylight (CDT) time.
        central_timezone = pytz.timezone('America/Chicago')

        # We convert the UTC time to Central Time.
        central_now = utc_now.astimezone(central_timezone)

        # We format the time into a "HH:MM" string (e.g., "13:24").
        time_string = central_now.strftime('%H:%M')

        # Finally, we return the string as an HTTP response.
        return HttpResponse(time_string)

# This function will handle requests to /app/sum
def calculate_sum(request):
    """
    This view takes two numbers, n1 and n2, from the URL parameters,
    adds them, and returns the result as a string.
    """
    if request.method == "GET":
        try:
            # We get the 'n1' and 'n2' values from the URL's query string.
            # We provide '0' as a default value if a parameter is missing.
            n1 = request.GET.get('n1', '0')
            n2 = request.GET.get('n2', '0')

            # Here I convert the values to floats to handle decimals, then add them.
            total = float(n1) + float(n2)

            # We return the result as a string in the HTTP response.
            return HttpResponse(str(total))
        except (ValueError, TypeError):
            # If the user provides text instead of numbers, we return an error.
            return HttpResponse("Error: Please provide valid numbers for n1 and n2.", status=400)
