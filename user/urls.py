from django.urls import path
from .views import register, get_users, getChannelName, filterUsers, getUser, updateUserDetails


urlpatterns = [
    path('register', register),
    path('get-users/<str:page>', get_users), 
    path('get-channel-name/<str:username>', getChannelName),
    path('filter-users/<str:pattern>', filterUsers), 
    path('get-user/<str:username>', getUser), 
    path('update-user/<str:username>', updateUserDetails)
]
