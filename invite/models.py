from django.db import models
from profiles.models import UserProfile

class Invitation(models.Model):
    owner = models.ForeignKey(UserProfile)
    email = models.EmailField(max_length=254)
    key = models.CharField(max_length=8)
    activated = models.BooleanField(default=False)
    message = models.TextField(max_length=1000, blank=True)

    def __unicode__(self):
        return self.email

    

