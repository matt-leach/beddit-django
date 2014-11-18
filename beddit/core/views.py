from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate
from django.contrib.auth import login as django_login
from django.contrib.auth import logout as django_logout
from django.conf import settings
from django.contrib.auth.models import User

from pyBeddit.clients import BedditClient

def home(request):
    try: print request.session["token"]
    except: pass
    print request.user
    # Check we have a token & a logged in user
    if "token" in request.session and request.user.id is not None:
        user = request.user
        context = {}
        return render(request, 'home.html', context)

    else:
        # We don't have a user. Show the authentication form
        context = {"form": AuthenticationForm()}
        return render(request, 'home.html', context)
    
    
def login(request):
    try:
        # see if we have valid username/password
        username = request.POST["username"]
        password = request.POST["password"]
    except:
        return redirect("home")
        
    # Custom authentication @ beddit.auth.BedditBackend
    user = authenticate(username=username, password=password, request=request)
    
    if user is not None:  
        django_login(request, user)
    else:
        messages.add_message(request, messages.INFO, "Your details could not be authenticated. Please try again.")
        
    return redirect("home")


def logout(request):
    try:
        # This will also remove the session
        django_logout(request)
        messages.add_message(request, messages.INFO, "Logged out successfully.")
    except:
        pass
    
    return redirect("home")    














    