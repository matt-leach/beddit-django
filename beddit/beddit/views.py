from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate
from django.contrib.auth import login as django_login
from django.contrib.auth import logout as django_logout
from django.conf import settings
from django.contrib.auth.models import User
from django.contrib import messages

from pyBeddit.clients import BedditClient

def home(request):
    # Check we have a token & a logged in user
    if "token" in request.session and request.user.id is not None:
        user = request.user
        context = {"username": user.username}

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
        
    user = authenticate(username=username, password=password)
    
    if user is not None:
        # We know this user. Log them in
        django_login(request, user)
        try:
            b = BedditClient(api_endpoint=settings.BEDDIT_API)
            token = b.get_token(username, password)    
            request.session["token"] = token
        except:
            django_logout(request)
            messages.add_message(request, messages.INFO, "Your details could not be authenticated.")
            # User cannot be verified.
            return redirect("home")
                
    else:
        # See if the username/password match a beddit account
        b = BedditClient(api_endpoint=settings.BEDDIT_API)
        try:
            # Get the user's token
            token = b.get_token(username, password)
            request.session["token"] = token
                        
            # Then create a user 
            try:
                # May have changed their password
                u = User.objects.get(username=username)
            except User.DoesNotExist:
                u = User.objects.create(username=username)
                
            u.set_password(password)
            u.save()
            django_login(request, u)
            messages.add_message(request, messages.INFO, "Login successful.")
        except: # TODO: Proper exception handling
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














    