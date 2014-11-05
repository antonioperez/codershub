from django.conf.urls import patterns, include, url
from django.contrib.auth.views import logout

from views import *

urlpatterns = patterns('',
    url(r'^$', FrontPage, name='home'),
    url(r'^logout/$', logout, {'next_page': '/'}),
    url(r'^login', LoginUser, name='login'),
    url(r'^register/$', RegisterUser, name='register'),
    url(r'^dashboard/$', DashboardView),
    url(r'^dashboard/import/$', DashboardImport),
    url(r'^user/(?P<user>[A-Za-z0-9]+)/$', UserPage),
)
