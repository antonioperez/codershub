from django.conf.urls import patterns, include, url
from django.contrib import admin
admin.autodiscover()

from users.views import *
from projects.views import *

urlpatterns = patterns('',
    # Examples:
    url(r'^addproject/', AddProject), #navigate here through the dashboard?
    url(r'^search/$',tabs),
    url(r'^search/(?P<error>[A-Za-z0-9]+)/$',tabs),
    url(r'^search/domain/(?P<language>[A-Za-z0-9_-]+)/$',search_by_domain),
    url(r'^search/user/(?P<username>[A-Za-z0-9]+)/$',search_by_user),
    url(r'^search/status/(?P<status>[A-Za-z0-9]+)/$',search_by_status),
    url(r'^search/project/(?P<project_name>[A-Za-z0-9_-]+)/$',search_by_project),
    url(r'^search/tag/(?P<tag>[A-Za-z0-9_-]+)/$',search_by_tag),
    
    url(r'^about_us/$', about_us_page),
    url(r'^projects/', include('projects.urls')),
    url(r'', include('users.urls')),

#dependances
    url(r'^tinymce/', include('tinymce.urls')),
    url(r'^activity/', include('actstream.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^messages/', include('django_messages.urls')),
)
