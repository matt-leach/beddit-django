from django.test import TestCase
from mock import patch, Mock

from django.test import RequestFactory
from django.contrib.auth.models import User

from django.contrib.messages.storage.fallback import FallbackStorage
from pyBeddit.clients import BedditClient
from django.contrib.auth import authenticate            
from copy import copy

class TestAuthentication(TestCase):
    
    
    def fake_get_token(self, username, password):
        """
        Mock get_token method
        """
        if username == "alice": return "alice token", 1
        
        elif username == "bob": return "bob token", 1
        
        elif username == "eve": raise Exception()
    
    def get_request(self):
        request = RequestFactory().get("")
        request.session = {}  
        request._messages = FallbackStorage(request)
        return request
        
    @patch.object(BedditClient, 'get_token', fake_get_token)
    def test_auth_user_does_not_exist(self):
        request = self.get_request()      
        
        user_created = authenticate(username="alice", password="password", request=request)
           
        # Check the token is in the session
        self.assertEqual(request.session["token"], "alice token")
           
        # Test now one user
        self.assertEqual(len(User.objects.all()), 1)
           
        u = User.objects.all()[0]
           
        self.assertEqual(user_created, u)
           
        self.assertEqual(u.username, "alice")
        self.assertEqual(u.password, "")
        self.assertEqual(u.is_superuser, False)


    @patch.object(BedditClient, 'get_token', fake_get_token)
    def test_auth_user_does_exist(self):
        request = self.get_request()      
            
        self.assertEqual(len(User.objects.all()), 0)
        
        u = User.objects.create(id=1, username="username")
                     
        user_got = authenticate(username="bob", password="password", request=request)
             
        # Check the token is in the session
        self.assertEqual(request.session["token"], "bob token")
             
        # Test still one user
        self.assertEqual(len(User.objects.all()), 1)
             
        self.assertEqual(user_got, u)
         
         
         
         
    @patch.object(BedditClient, 'get_token', fake_get_token)    
    def test_get_token_failed(self):
        
        request = self.get_request()                          
              
        user = authenticate(username="eve", password="password", request=request)
        
        # Failed auth should return no user
        self.assertTrue(user is None)
        
        # Check messages
        self.assertEqual(len(list(request._messages)), 1)
        message = list(request._messages)[0]
        self.assertEqual(str(message), "Your details could not be authenticated. Please try again.")
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            