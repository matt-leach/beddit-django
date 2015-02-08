from django.conf.urls import url

from sleeps import views

urlpatterns = [
    url(r'^$', views.stacked, name='stacked'),
]
