from django.db import models

class MediaModel(models.Model):
    pic = models.ImageField(upload_to='profilepics', blank=True, null=True)