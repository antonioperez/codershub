from django.shortcuts import render, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect

from users.models import *
from users.forms import *
from projects.models import *

from actstream import action
from actstream.models import user_stream, following, followers
from actstream.actions import follow, unfollow


import urllib2
import json 
import requests

def FrontPage(request):
    return render(request, 'front_page.html')

def LoginUser(request):
    error = False
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username,
                            password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                if request.GET.get('next'):
                    return HttpResponseRedirect(request.GET.get('next'))
                else:
                    return HttpResponseRedirect("/dashboard")
                
        error = True
    return render(request, 'login.html',  {'error': error,})


def RegisterUser(request):
    if request.method == 'POST':
        mainuser_form = MainUserForm(request.POST)
        hubuser_form = HubUserForm(request.POST)

        if mainuser_form.is_valid() and hubuser_form.is_valid():
            user_cd = mainuser_form.cleaned_data
            new_user = User.objects.create_user(username=user_cd['username'],
                                                password=user_cd['password'],
                                                first_name=user_cd['first_name'],
                                                last_name=user_cd['last_name'])
            new_hubuser = hubuser_form.save(commit=False)
            new_hubuser.user = new_user
            new_hubuser.save()
            user = authenticate(username=user_cd['username'],
                                password=user_cd['password'])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    action.send(request.user, verb="Joined Coderzhub.")
                    return HttpResponseRedirect("/dashboard")
    else:
        mainuser_form = MainUserForm()
        hubuser_form = HubUserForm()
    return render(request, 'register.html', {'mainuser_form': mainuser_form,
                                             'hubuser_form': hubuser_form})


#def user_page(request, user_id):
#    stream = user_stream(request.user)
#    user_name = HubUser.objects.get(user__id=user_id)
#    github_request = urllib2.urlopen('https://api.github.com/users/%s'
#                                     % (user_name.github))
#    json_data = json.loads(github_request.read())
#    github_login = json_data['login']
#    github_email = json_data['email']
#    return render(request, 'user_page.html', {'user_name': user_name.user,
#                                              'github_username': github_login,
#                                              'github_email': github_email,
#                                              'stream' : stream,})


def UserPage(request, user):
    try:
        user_name = HubUser.objects.get(user__id=int(user))
    except ValueError:
        user_name = HubUser.objects.get(user__username__iexact=user)
    
    stream = user_stream(user_name.user)
    github_request = urllib2.urlopen('https://api.github.com/users/%s' 
                                     % (user_name.github))
    json_data = json.loads(github_request.read())
    github_login = json_data['login']
    if 'email' in json_data:
        github_email = json_data['email']
    else:
        github_email = ''
    
    try:
        visitor = HubUser.objects.get(user__username__iexact=request.user.username)
    except:
        visitor = None
    
    is_following = False
    if visitor != None:
        follow_list = following(visitor.user)
        if user_name in follow_list:
            is_following = True
        
    if (request.GET.get('follow_button')):
        if user_name in follow_list:
            unfollow(visitor.user, user_name)
            action.send(visitor, verb='unfollowed', target=user_name)
            HttpResponseRedirect(request.path)
        else:
            follow(visitor.user, user_name)
            HttpResponseRedirect(request.path)
            
    stream = user_stream_page_filter(user_name.user)
    if visitor != None:
        visitor = visitor.user
    print stream
    return render(request, 'user_page.html', {'user_name': user_name.user,
                                              'github_username': github_login,
                                              'github_email': github_email,
                                              'stream' : stream,
                                              'visitor' : visitor,
                                              'is_following' : is_following, })
    
def DashboardView(request):
    if request.user.is_authenticated():
        hubuser = HubUser.objects.get(user__username__iexact=request.user.username)
        repo_list = Project.objects.filter(owners=hubuser)
        return render(request, 'dashboard.html', {'user_name': hubuser.user,
                                                  'github_username': hubuser.github,
                                                  'repo_list': repo_list})
    else:
        return HttpResponseRedirect("/login")


def user_stream_page_filter(page_owner):
    me = HubUser.objects.get(user__username__iexact=page_owner.username)
    my_actions1 = user_stream(me)
    my_actions2 = user_stream(me.user)
    filtered_actions = []
    if my_actions1.exists():
        my_actions=my_actions1
    else:
        my_actions=my_actions2
        
    for a in my_actions:
        if a.actor == me.user or a.actor == me:
            filtered_actions.append(a)
    
    for a in my_actions:
        if a.target == me.user or a.target == me:
            filtered_actions.append(a)
    
    filtered_actions.sort(key=lambda x: x.timestamp, reverse=True)
    return filtered_actions
    
    
def user_dashboard_filter(page_owner):
    me = HubUser.objects.get(user__username__iexact=page_owner.username)
    my_actions = user_stream(me)
    filtered_actions = []
    
    for a in my_actions:
        if a.actor == me.user or a.actor == me:
            filtered_actions.append(s)
    
    for a in my_actions:
        if a.target == me.user or a.target == me:
            filtered_actions.append(s)
    
    
    filtered_actions.sort(key=lambda x: x.timestamp, reverse=True)
    return filtered_actions

def DashboardImport(request):
    if request.user.is_authenticated():
        if request.method == 'POST':
            import_project_form = ImportProjectForm(request.POST, request=request)
            if import_project_form.is_valid():
                project_cleaned = import_project_form.cleaned_data
                user = HubUser.objects.get(user__username__iexact=request.user.username)
                github_request = urllib2.urlopen('https://api.github.com/repos/%s/%s' % (user.github, project_cleaned['name']))
                json_data = json.loads(github_request.read())
               
                new_project = Project.objects.create(name=project_cleaned['name'],
                                                    status=project_cleaned['status'],
                                                    descript=json_data['description'],
                                                    language=json_data['language'],
                                                    version='1.0',
                                                    created_on=json_data['created_at'],
                                                    url=json_data['url'],
                                                    )
                
                user = HubUser.objects.get(user__username__iexact=request.user.username)
                new_project.owners.add(user)
                new_project.save()
                Forum(project=new_project).save()
                action.send(request.user, verb="Added a project.")
                return HttpResponseRedirect("/dashboard")
            else:
                return render(request, 'dashboard_import.html', {'import_project_form': import_project_form})
        else:
            import_project_form = ImportProjectForm(request=request)
            return render(request, 'dashboard_import.html', {'import_project_form': import_project_form})
    else:
        return HttpResponseRedirect("/login")
