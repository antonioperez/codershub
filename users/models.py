from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class HubUser(models.Model):
    user = models.OneToOneField(User)
    github = models.CharField(max_length=39)
    github_password = models.CharField(max_length=100)
    
    def __unicode__(self):
        return unicode(self.user)