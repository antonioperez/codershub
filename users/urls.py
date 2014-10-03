from django.conf.urls import patterns, include, url

from views import *

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'coderzhub.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^register/$', RegisterUser, name='register'),
    url(r'^login', LoginUser, name='login'),
    url(r'^dashboard/$', dashboard_view),
    url(r'^dashboard/import/$', dashboard_import),
    url(r'^(?P<user>[A-Za-z0-9]+)/$', user_page),
)
