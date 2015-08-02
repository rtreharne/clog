from django.db import models
from django.contrib.auth.models import User
from profiles.models import UserProfile
from django.utils import timezone
from time import time

class Project(models.Model):
    owner = models.ForeignKey(UserProfile)
    title = models.CharField(max_length=50)
    description = models.TextField(max_length=200)
    start_date = models.DateTimeField(default=timezone.datetime.today())
    updated = models.DateTimeField(default=timezone.datetime.today())
    def __unicode__(self):
        return self.title
