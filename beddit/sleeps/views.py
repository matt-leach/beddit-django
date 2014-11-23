from django.http import HttpResponse
from pyBeddit.clients import BedditClient
from django.shortcuts import redirect, render
from django.conf import settings
import json
from datetime import datetime

from core.decorators import requires_token

def convert_date_format(date_string):
    """
    converts YYYY-MM-DD to DD/MM
    """
    return datetime.strptime(date_string, '%Y-%m-%d').strftime('%d/%m')

@requires_token
def index(request):
            
    b = BedditClient(api_endpoint=settings.BEDDIT_API, token=request.session["token"], user_id=request.user.id)
            
    sleep_data = b.get_sleep_scores()
    
    data = [{"date": convert_date_format(date), "score": score} for date, score in sleep_data.items()]
    
    context = {"data": json.dumps(data)}

    return render(request, 'sleeps/index.html', context)
    
