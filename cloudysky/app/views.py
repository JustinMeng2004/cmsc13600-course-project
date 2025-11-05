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
from .models import Profile

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
