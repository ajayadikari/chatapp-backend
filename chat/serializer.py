from rest_framework.serializers import ModelSerializer
from .models import ChatModel

class ChatSerializer(ModelSerializer):
    class Meta:
        model = ChatModel
        fields = ['sender', 'receiver', 'is_file', 'text', 'file','timestamp']