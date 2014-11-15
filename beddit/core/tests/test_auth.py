from django.test import TestCase
from mock import patch
from django.contrib.auth import authenticate


class TestAuthentication(TestCase):
    
    
    def test_wrong_auth(self):
        
        with patch('pyBeddit.clients.BedditClient') as MockClient:
            pass
            