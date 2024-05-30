from django.db import models

class ChatModel(models.Model):
    sender = models.TextField(null=False)
    receiver = models.TextField(null=False)
    # msg = models.TextField(null=False)
    is_file = models.BooleanField(null=False, blank=False, default=False)
    text = models.TextField(null=True, blank=True)
    file = models.FileField(upload_to='files/', null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
