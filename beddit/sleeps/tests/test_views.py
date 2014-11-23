from django.test import TestCase
from django.test.client import RequestFactory
from model_mommy import mommy
from django.contrib.auth.models import User
from sleeps.views import index
from pyBeddit.clients import BedditClient
from mock import patch
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse

class TestSleepsIndexWithRequestFactory(TestCase):
    
    # Patch the get_sleep_scores function to return an empty dictionary
    @patch.object(BedditClient, 'get_sleep_scores', lambda x: {})
    def test_index_requires_token(self):
        request = RequestFactory().get("/sleeps/")
        request.session = {"token": "TOKEN"}
        request.user = mommy.make(User)
        
        resp = index(request)
        self.assertEqual(resp.status_code, 200)
        
    @patch.object(BedditClient, 'get_sleep_scores', lambda x: {})  
    def test_index_no_token(self):
        request = RequestFactory().get("/sleeps/")
        request.session = {}
        request.user = mommy.make(User)
        
        # Check it redirects to Home
        resp = index(request)
        self.assertEqual(type(resp), HttpResponseRedirect)
        self.assertEqual(resp["Location"], reverse("home"))
        
    @patch.object(BedditClient, 'get_sleep_scores', lambda x: {})  
    def test_index_no_user(self):
        request = RequestFactory().get("/sleeps/")
        request.session = {"token": "TOKEN"}
        request.user = None
        
        resp = index(request)
        self.assertEqual(resp, HttpResponseRedirect)
        self.assertEqual(resp["Location"], reverse("home"))