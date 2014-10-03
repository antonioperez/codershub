from django.conf.urls import patterns, include, url

from views import *
urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'coderzhub.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),/view/topics/
    url(r'^$', ProjectDashboard, name='Create Forum'),
    url(r'^(?P<project_id>\d+)/$',Project_Page),
    url(r'^(?P<project_id>\d+)/create/topic/$', CreateTopic, name='Create Topic'),
    url(r'^(?P<project_id>\d+)/view/topics/$', ViewTopic, name='View Topic'),
    url(r'^(?P<topic_id>\d+)/discussion/$', Discussion, name='Discussion Topic'),
    url(r'^(?P<username>[A-Za-z0-9]+)/repos/$', user_repo_list),
    url(r'^domain/(?P<language>[A-Za-z0-9_-]+)/$',search_by_domain),
    url(r'^user/(?P<username>[A-Za-z0-9]+)/$',search_by_user),
    url(r'^status/(?P<status>[A-Za-z0-9]+)/$',search_by_status),
    url(r'^project/(?P<project_name>[A-Za-z0-9_-]+)/$',search_by_project),
    #url(r'^(?P<username>[A-Za-z0-9]+)/(?P<repo>[A-Za-z0-9_-]+)/$', repo_view),
)
