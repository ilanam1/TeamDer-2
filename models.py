from django.db import models

class Bio(models.Model):
    bio = models.TextField()
    profile_pic = models.ImageField(upload_to='profile_pics/')
