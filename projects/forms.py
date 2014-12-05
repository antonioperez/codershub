from django.contrib.auth.models import User
from django.forms.util import ErrorList
from django import forms
from projects.models import *
from users.models import HubUser

from django.forms import ModelForm
import datetime

from tinymce.widgets import TinyMCE
from django.forms.formsets import formset_factory


class ForumForm(forms.ModelForm):
    class Meta:
        model = Forum
        fields = ('name','content')
        widgets = {
            'content': TinyMCE(attrs={'cols': 20, 'rows': 10, 'class':'comment_text'}),
        }
        
class TopicForm(forms.ModelForm):
    class Meta:
        model = Topic
        fields = ('topic','content')
        widgets = {
            'content': TinyMCE(attrs={'cols': 20, 'rows': 10, 'class':'comment_text'}),
        }

        
class CommentForm(forms.ModelForm):
    content1 = forms.CharField(widget=TinyMCE(attrs={'cols': 20, 'rows': 20, 'class':'comment_text'}))
    class Meta:
        model = Comment
        fields = ('content',)
        widgets = {
            'content': TinyMCE(attrs={'cols': 20, 'rows': 10, 'class':'comment_text'}),
        }

# Create your models here.
class ProjectForm(forms.ModelForm):
    github_password = forms.CharField(widget = forms.PasswordInput, max_length = 30)
    class Meta:
        model = Project
        fields = ['name', 'github_password', 'owners', 'descript', 'language', 'status', 'version', ]
        created_on = datetime.datetime.now()
        widgets = {
            'github_password': forms.PasswordInput(),
        }

class UpdateProject(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['name','owners','descript', 'language', 'status', 'version',]
        
class TagForm(ModelForm):
    model = Tag
    fields = [Tag]
        
CommentFormSet = formset_factory(CommentForm)