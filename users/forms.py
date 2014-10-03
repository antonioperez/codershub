from django.contrib.auth.models import User
from django.forms.util import ErrorList
from django import forms
from users.models import *
from projects.models import Project
import requests
from django.contrib.auth.hashers import make_password 


class MainUserForm(forms.ModelForm):
    verify_password = forms.CharField(widget=forms.PasswordInput())
    class Meta:
        model = User
        fields = ('username','password','verify_password','first_name', 'last_name')
        widgets = {
            'password': forms.PasswordInput(),
            'verify_password': forms.PasswordInput(),
        }

    def clean_username(self):
        existing_user = User.objects.filter(username=self.cleaned_data['username']) 
        if existing_user.exists():
            raise forms.ValidationError("Username already registered.")
        else:
            return self.cleaned_data['username']
        
    def clean(self): 
        
        d = self.cleaned_data
        e = self._errors

        if 'password' in self.cleaned_data and 'verify_password' in self.cleaned_data:
            if self.cleaned_data['password'] != self.cleaned_data['verify_password']:
                self._errors['password'] = ErrorList(["The two password fields didn't match."])
    
            elif len(self.cleaned_data['password']) < 6:
                self._errors['password'] = ErrorList(["Password must be 6 or more characters."])
        return self.cleaned_data
    
class HubUserForm(forms.ModelForm):
    github_pass_var = forms.CharField(widget=forms.PasswordInput(), label= "Verify Git Pasword")
    class Meta:
        model = HubUser
        fields = ('github','github_password','github_pass_var',)
        widgets = {
            'github_password': forms.PasswordInput(),
            'github_pass_var': forms.PasswordInput(),
        }
        
        
    def clean(self): 
        
        d = self.cleaned_data
        e = self._errors

        if ('github_password' in self.cleaned_data and 'github_pass_var' in self.cleaned_data):
            if self.cleaned_data['github_password'] != self.cleaned_data['github_pass_var']:
                self._errors['github_password'] = ErrorList(["The two password fields didn't match."])
    
            elif len(self.cleaned_data['github_password']) < 6:
                self._errors['github_password'] = ErrorList(["Password must be 6 or more characters."])
            elif (verify_github( self.cleaned_data['github'], self.cleaned_data['github_password']) == False):
                self._errors['github'] = ErrorList("Not a valid Github")
            else:
                crypted_pass = make_password(self.cleaned_data['github_password'])
                self.cleaned_data['github_password'] = crypted_pass
        return self.cleaned_data
    
    
def verify_github(git_handle, git_pass):
    r = requests.get('https://api.github.com',auth=(git_handle, git_pass))
    if(r.status_code == 200):
        return True
    else:
        return False
    
    
#HubUserFormSet = forms.models.inlineformset_factory(User, HubUser)
class ImportProjectForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request")
        super(ImportProjectForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Project
        fields = ('name','status')
        widgets = {
            
        }

    def clean_name(self):
        user = HubUser.objects.get(user__username__iexact=self.request.user.username)
        existing_project = Project.objects.filter(name=self.cleaned_data['name']).filter(owners=user)
        if existing_project.exists():
            raise forms.ValidationError("That repository is already registered.")
        else:
            return self.cleaned_data['name']
