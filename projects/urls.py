from django.conf.urls import patterns, include, url

from views import *
urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'coderzhub.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),/view/topics/
    url(r'^$', ProjectDashboard, name=''),
    url(r'^forums/$', PublicForums, name='Public Forums'),
    url(r'^create/forum/$', CreateForum, name='Create Forum'),
    url(r'^(?P<project_id>\d+)/$',ProjectPage),
    url(r'^(?P<project_id>\d+)/edit/$', EditProject, name='Create Topic'),
    url(r'^(?P<project_id>\d+)/create/topic/$', CreateTopic, name='Create Topic'),
    url(r'^(?P<project_id>\d+)/view/topics/$', ViewTopic, name='View Topic'),
    url(r'vote/$', VoteTopic, name='Vote Topic'),
    
    url(r'^(?P<topic_id>\d+)/discussion/$', Discussion, name='Discussion Topic'),
    url(r'^(?P<username>[A-Za-z0-9]+)/repos/$', user_repo_list),
    #url(r'^(?P<username>[A-Za-z0-9]+)/(?P<repo>[A-Za-z0-9_-]+)/$', repo_view),
)
