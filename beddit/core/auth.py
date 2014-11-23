from django.conf import settings
from django.contrib import messages
from django.contrib.auth.models import User
from pyBeddit.clients import BedditClient


class BedditBackend(object):
    """
        Backend authentication which uses the Beddit API Auth.
        
        Checks username/password.
        
        If successful a token will be added to the session which we use
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
            
        except Exception: # TODO: more detailed exception
            return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None