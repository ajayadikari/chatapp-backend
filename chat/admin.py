from django.contrib import admin
from .models import ChatModel

class ChatAdmin(admin.ModelAdmin):
    # list_display = ('sender', 'receiver', 'msg', 'timestamp')
    list_display = ('sender', 'receiver', 'text', 'file', 'timestamp')

admin.site.register(ChatModel, ChatAdmin)