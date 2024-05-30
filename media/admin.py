from django.contrib import admin
from .models import MediaModel


class MediaAdmin(admin.ModelAdmin):
    list_display = ['profilepic']

    def profilepic(self, obj):
        return f'<img src="{obj.pic.url}" height="100" width="100px">'
    

admin.site.register(MediaModel, MediaAdmin)