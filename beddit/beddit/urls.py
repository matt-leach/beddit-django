from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'beddit.views.home', name='home'),
    url(r'^login/$', 'beddit.views.login', name='login'),
    url(r'^logout/$', 'beddit.views.logout', name='logout'),
    url(r'^sleeps/$', include('sleeps.urls'), name="sleeps")
    # url(r'^blog/', include('blog.urls')),

    # url(r'^admin/', include(admin.site.urls)),
    
)
