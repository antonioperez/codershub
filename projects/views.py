from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect
from actstream import action
from actstream.actions import follow, unfollow
from django.template import RequestContext


from projects.models import *
from projects.forms import *
from users.models import HubUser

from django.contrib.auth.hashers import check_password
import requests, json, urllib2
import datetime


def CreateTopic(request, project_id):
    project = get_object_or_404(Project, id=project_id)
    if request.method == 'POST':
        topic_form = TopicForm(request.POST)
        if topic_form.is_valid():
            new_topic = topic_form.save(commit=False)
            new_topic.forum = project.forum
            new_topic.save()
            return HttpResponseRedirect('/projects/%s/view/topics/' % project.id)
    else:
        topic_form = TopicForm()
    return render(request, 'forum/add_topic.html', {'topic_form': topic_form,})

def ViewTopic(request, project_id):
    project = get_object_or_404(Project, id=project_id)
    topics = Topic.objects.filter(forum=project.forum.id)
    if request.method == 'POST':
        # delete/edit topic stuff
        pass
        
    return render(request, 'forum/view_topics.html', {'project':project, 
                                                      'topics':topics})


def Discussion(request, topic_id):
    topic = get_object_or_404(Topic, id=topic_id)
    comments = Comment.objects.filter(parent=None)
    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        comment = request.POST.get('content')
        if comment_form.is_valid() or comment:
            cparent = request.POST.get('cparent')
            new_comment = Comment(content=comment)           
            cparent = request.POST.get('cparent')
            if cparent:
                cparent = Comment.objects.get(id=cparent)
                new_comment.parent = cparent
        
            new_comment.commenter = request.user.hubuser
            new_comment.topic = topic
            new_comment.save()
            return HttpResponseRedirect("")
                
    else:
        comment_form = CommentForm()
    return render(request, 'forum/discussion.html', {'topic':topic, 
                                                     'comments': comments, 
                                                     'comment_form':comment_form})

    

def ProjectDashboard(request):
    return render(request, 'dashboard.html')

def Project_Page(request, project_id):
    project = get_object_or_404(Project, id=int(project_id))
    
    return render(request, 'project_page.html', {'project': project})
    
    
def user_repo_list(request, username):
    user = HubUser.objects.get(user__username__iexact=username)
    repo_list = Project.objects.filter(owners=user)
    
    return render(request, 'repo_list.html', {'user_name': user.user,
                                              'repo_list': repo_list})


def repo_view(request, username, repo):
    user = HubUser.objects.get(user__username__iexact=username)
    project_details = Project.objects.get(name=repo, owners=user)
    github_request = urllib2.urlopen('https://api.github.com/repos/%s/%s' % (user.github, repo))
    json_data = json.loads(github_request.read())

    return render(request, 'repo_view.html', {'owner': json_data['owner']['login'],
                                              'name': json_data['name'],
                                              'description': json_data['description'],
                                              'url': json_data['url'],
                                              'created_at': json_data['created_at'],
                                              'updated_at': json_data['updated_at']
                                              })



# Create your views here.
def search_by_user(request, username):
    users = HubUser.objects.filter(user__username__icontains=username) | HubUser.objects.filter(github__icontains=username)
    if users:
        user_list = []
        for user in users:
            projects = Project.objects.filter(owners=user)
            user_list.append({'username': user.user, 'github_name': user.github, 'project_count': projects.count()})
        return render(request, 'search_list.html', {'user_name': username,
                                                'user_list': user_list})
    else:
        return HttpResponseRedirect('/search_tabs/error')
    
def search_by_domain(request, language):
    projects_list = Project.objects.filter(language__icontains=language)
    if projects_list:
        return render(request, 'search_domain.html', {'language': language,
                                                  'projects_list': projects_list,
                                                  })
    else:
        return HttpResponseRedirect('/search_tabs/error')

def search_by_status(request, status):
    projects_list = Project.objects.filter(status = status)
    if projects_list:
        return render(request, 'search_status.html', {'status': status,
                                                  'projects_list': projects_list})
    else:
        return HttpResponseRedirect('/search_tabs/error')
    
def search_by_project(request, project_name):
    projects_list = Project.objects.filter(name__icontains = project_name)
    if projects_list:
        return render(request, 'search_project.html', {'project_name': project_name,
                                                   'projects_list': projects_list})
    else:
        return HttpResponseRedirect('/search_tabs/error')





# Create your views here.

def Project_Form(request):
    if request.method == 'POST':
        form = ProjectForm(request.POST, request.FILES) 
        
        if form.is_valid() and github_create(request, form):
            form.save()
            action.send(request.user, verb='added a Project!')
            t=HubUser.objects.get(user__username__iexact='somuser')
            follow(request.user, t)
            redurl = '/' + str(request.user) + '/repos'
            
            return HttpResponseRedirect(redurl)
    else:
        form = ProjectForm()
        
    return render(request, 'add_project.html', {
            "form":form,
        }, context_instance=RequestContext(request))


def github_create(request, form):
    username = request.user.username
    user_git = HubUser.objects.get(user__username__iexact = username)
    if check_password(form.cleaned_data['github_password'], user_git.github_password):
        github_url = "https://api.github.com/" + user_git.github +"/repos"
        data = json.dumps({'name' : form.cleaned_data['name'], 'description' : form.cleaned_data['descript']})
        r = requests.post(github_url, data, auth=(user_git.github, form.cleaned_data['github_password']))
        return True
    else:
        form._errors['github_password'] = "Password incorrect"
        return False
    
def tabs(request, error=""):
    if request.method=="POST":
        var= request.POST.get("status")
        if var:
            redurl = '/search/status/'+ var
            return HttpResponseRedirect(redurl)
        var= request.POST.get("project")
        if var:
            redurl = '/search/project/'+ var
            return HttpResponseRedirect(redurl)
        var= request.POST.get("domain")
        if var:
            redurl = '/search/domain/'+ var
            return HttpResponseRedirect(redurl)
        var= request.POST.get("user")
        if var:
            redurl = '/search/user/'+ var
            return HttpResponseRedirect(redurl)
    
    return render(request, 'tabs.html', {'error': error})


def about_us_page(request):
    return render(request, 'about_us.html')


