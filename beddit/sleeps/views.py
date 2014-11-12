from django.http import HttpResponse
from pyBeddit.clients import BedditClient
from django.shortcuts import redirect, render
from django.conf import settings

def index(request):
    
    if "token" in request.session and request.user.id is not None:
        
        b = BedditClient(api_endpoint=settings.BEDDIT_API, token=request.session["token"], user_id=request.user.id)
                
        sleep_data = b.get_sleep_scores()
        print sleep_data
        
        context = {"data": sleep_data}

        return render(request, 'sleeps/index.html', context)
    
    else:
        return redirect("home")