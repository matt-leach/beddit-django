from django.conf import settings
from django.contrib.auth.models import User
from pyBeddit.clients import BedditClient
from django.contrib import messages


class BedditBackend(object):
    """
    
    """

    def authenticate(self, username=None, password=None, request=None):
        
        b = BedditClient(api_endpoint=settings.BEDDIT_API)
        try:
            token, user_id = b.get_token(username, password)    
            request.session["token"] = token
            
            try:
                user = User.objects.get(id=user_id)
                user.username = username
                user.save()
                
            except User.DoesNotExist:
                user = User(username=username, id=user_id)
                user.save()
                
            return user
            
        except: # TODO: more detailed exception
            messages.add_message(request, messages.INFO, "Your details could not be authenticated. Please try again.")
            return None
        
            
            
          
        
        
        
        
        
        


    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None