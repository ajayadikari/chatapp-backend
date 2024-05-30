from django.urls import path
from .views import storeMsg, fetchChat

urlpatterns = [
    path('store-msg/<str:file>', storeMsg), 
    path('fetch-chats/<str:sender>/<str:receiver>', fetchChat)
]
