from django.shortcuts import render

# Create your views here.
# app/views.py

from django.http import HttpResponse
from datetime import datetime
import pytz # A library to handle timezones

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
