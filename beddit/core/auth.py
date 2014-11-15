from django.conf import settings
from django.contrib.auth.models import User
from pyBeddit.clients import BedditClient
from django.contrib import messages


class BedditBackend(object):
    """
        Backend authentication which uses the Beddit API Auth.
        
        Checks username/password.
        
        If successful a token will be returned which we use to 
        access the API.
        
        This ensures we do NOT store passwords anywhere.
    """

    def authenticate(self, username=None, password=None, request=None):
        
        b = BedditClient(api_endpoint=settings.BEDDIT_API)
        try:
            # See if this username/password is valid
            token, user_id = b.get_token(username, password)   
                         
            try:
                # First see if this user exists
                user = User.objects.get(id=user_id)
                
                # update username
                user.username = username
                user.save()
                
            except User.DoesNotExist:
                # Otherwise create the user
                user = User(username=username, id=user_id)
                user.save()
                
            request.session["token"] = token  
            return user
            
        except: # TODO: more detailed exception
            messages.add_message(request, messages.INFO, "Your details could not be authenticated. Please try again.")
            return None
        
            
            
          
        
        
        
        
        
        


    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None