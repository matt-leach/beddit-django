from django.http import HttpResponse
from pyBeddit.clients import BedditClient
from django.shortcuts import redirect, render
from django.conf import settings
import json
from datetime import datetime

import datetime

from core.decorators import requires_token


def convert_date_format(date_string):
    """
    converts YYYY-MM-DD to DD/MM
    """
    return datetime.strptime(date_string, '%Y-%m-%d').strftime('%d/%m')

def convert_epoch_to_time_after_3pm(secs):
    t = datetime.datetime.fromtimestamp(secs)
    from_3 = t - t.replace(hour=15, minute=0, second=0)

    
    return from_3.seconds / 3600.0 # Return in hours


@requires_token
def index(request):
            
    b = BedditClient(api_endpoint=settings.BEDDIT_API, token=request.session["token"], user_id=request.user.id)
    
    sleep_data = b.get_sleep_scores()
    
    data = [{"date": convert_date_format(date), "score": score} for date, score in sleep_data.items()]
    
    context = {"data": json.dumps(data)}

    return render(request, 'sleeps/index.html', context)
    

@requires_token
def stacked(request):
    # Not recording, Away, asleep, Awake, Break
    
    
    b = BedditClient(api_endpoint=settings.BEDDIT_API, token=request.session["token"], user_id=request.user.id)
    
    sleeps = b.requestor.get_all_sleeps("2000-01-01", "2020-01-01")
    
    data = []
    for sleep in sleeps.json():
        date = sleep['date']
        zones = sleep["time_value_tracks"]["sleep_stages"]["items"]
        zones.append([sleep["end_timestamp"], 0])
        
        new_zones = []
        
        
        y0 = 0
        name = 0
        for z in zones:
            y1 = convert_epoch_to_time_after_3pm(z[0])
            
            new_zones.append({"name": name, "y0": y0, "y1": y1})
            y0 = y1
            name = z[1]
        
        new_zones.append({"name": 0, "y0": y0, "y1": 24})
        
        data.append({"date": date, "zones": new_zones})
        
        
        
        
    return render(request, 'sleeps/stacked.html', {"data": json.dumps(data)})







