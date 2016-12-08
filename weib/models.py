from __future__ import unicode_literals

from django.db import models

# Create your models here.

class users(models.Model):
    uid = models.CharField(max_length=200)
    name = models.CharField(max_length=50)
    image_url = models.TextField()
    statuses_count = models.IntegerField()
    friends_count = models.IntegerField()
    followers_count = models.IntegerField()
    verified = models.BooleanField()
    verified_type = models.IntegerField()
    auth_token = models.TextField()
    expired_time = models.FloatField()
    
class ss(models.Model):
    uid = models.CharField(max_length=200)
    name = models.CharField(max_length=50)
    img = models.ImageField(upload_to='upload')
    status = models.TextField()
