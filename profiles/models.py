from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from time import time
from sorl.thumbnail import get_thumbnail, ImageField

class UserProfile(models.Model):
    user = models.OneToOneField(User)
    affiliation = models.CharField(max_length=128, blank = True)
    picture = ImageField(upload_to='user_images', default='static/img/avatar.png')
    url = models.URLField(blank=True)
    linkedin = models.URLField(blank=True)
    twitter = models.URLField(blank=True)
    bio = models.TextField(max_length=2000, blank=True)

    def __unicode__(self):
        return self.user.username
