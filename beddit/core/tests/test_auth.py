from django.test import TestCase
from mock import patch
from django.contrib.auth import authenticate
from django.test import RequestFactory
from django.contrib.auth.models import User

class TestAuthentication(TestCase):
    
    
    def test_auth_user_does_not_exist(self):
        
        User.objects.all().delete()
    
        with patch('pyBeddit.clients.BedditClient') as mock:
            
            MockClient = mock.return_value
            
            # Needs to return token, user_id
            MockClient.get_token.return_value = "TOKEN", 1
                        
            request = RequestFactory().get("")
            request.session = {}
            
            authenticate(username="username", password="password", request=request)
            
            # Check the token is in the session
            self.assertEqual(request.session["token"], "TOKEN")
            
            # Test now one user
            self.assertEqual(len(User.objects.all()), 1)
            
            # Test user has: 
            # correct username
            # NO password
            # not superuser
            u = User.objects.all()[0]
            self.assertEqual(u.username, "username")
            self.assertEqual(u.password, "")
            self.assertEqual(u.is_superuser, False)
            
            
    def test_auth_user_does_exist(self):
        
        User.objects.all().delete()
        User.objects.create(id=1, username="username")
    
        with patch('pyBeddit.clients.BedditClient') as mock:
            
            MockClient = mock.return_value
            
            # Needs to return token, user_id
            MockClient.get_token.return_value = "TOKEN", 1
                        
            request = RequestFactory().get("")
            request.session = {}
            
            authenticate(username="username", password="password", request=request)
            
            # Check the token is in the session
            self.assertEqual(request.session["token"], "TOKEN")
            
            # Test still one user
            self.assertEqual(len(User.objects.all()), 1)
            
            # Test user has: 
            # correct username
            # NO password
            # not superuser
            u = User.objects.all()[0]
            self.assertEqual(u.username, "username")
            self.assertEqual(u.password, "")
            self.assertEqual(u.is_superuser, False)
            
            
            
            
            
            
            
            