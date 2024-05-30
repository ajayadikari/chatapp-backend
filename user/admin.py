from django.contrib import admin
from django.utils.html import mark_safe
from .models import UserModel

class UserAdmin(admin.ModelAdmin):
    list_display=('id', 'username', 'channel_name', 'display_profile_pic')

    def display_profile_pic(self, obj):
        if obj.profile_pic:
            return mark_safe('<img src="{}" width="100" height="50" />'.format(obj.profile_pic.pic.url))
        else:
            return "No pic"
admin.site.register(UserModel, UserAdmin)