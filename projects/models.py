from django.db import models
from users.models import *

import datetime
from tinymce.models import HTMLField
import PIL as Image

    
class Project(models.Model):
    STATUS_CHOICES = (
        ('initial', 'initial'),
        ('bug', 'Buggy'),
        ('help', 'HELP'),
        ('complete', 'complete, refining'),
    )

    owners = models.ManyToManyField(HubUser, related_name='o+')
    name = models.CharField(null=True, max_length=100)
    descript = HTMLField()
    language = models.CharField(null=True, max_length = 100)
    url = models.CharField(null = True, max_length=100)
    status = models.CharField(choices = STATUS_CHOICES, default='initial', max_length=60)
    version = models.CharField(null=True, max_length=15)
    subscribers = models.ManyToManyField(HubUser, related_name='s+', blank=True)
#    icon = models.ImageField(blank=True, upload_to='media/')
    created_on = models.DateTimeField(auto_now_add = False)

    def __unicode__(self):
        return self.name
    
    
class Tag(models.Model):
    project = models.ForeignKey(Project)
    tag = models.CharField(null=True, max_length=30)
    
    
class Forum(models.Model):
    project = models.OneToOneField(Project)
    name = models.CharField(blank=True, max_length=100)

class Topic(models.Model):
    forum = models.ForeignKey(Forum)
    topic = models.CharField(max_length=100)
    content = HTMLField()
    order = models.IntegerField(default = 0)
    votes = models.IntegerField(default = 0)
    
class Comment(models.Model):
    topic = models.ForeignKey(Topic)
    commenter = models.ForeignKey(HubUser)
    content = HTMLField()
    parent = models.ForeignKey('self', blank=True, null=True)
    order = models.IntegerField(default = 0)
    created = models.DateTimeField(auto_now_add=True)
    votes = models.IntegerField(default = 0)
    #votes/score?
    
    def thread_comments(self):
        comments = self.objects.filter(id=self.id)



    
        
        
        
        
        
        
        
        
        
