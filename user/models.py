from django.db import models
from django.contrib.auth.models import AbstractUser, PermissionsMixin
from media.models import MediaModel

class UserModel(AbstractUser, PermissionsMixin):
    channel_name = models.TextField(unique=True, null=True)
    profile_pic = models.OneToOneField(MediaModel, null=True, blank=True, unique=True, on_delete=models.CASCADE)
