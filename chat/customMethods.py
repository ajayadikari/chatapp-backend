from .models import ChatModel
from django.db.models import Q
from .serializer import ChatSerializer


def store(chatDetails, file):
    try:
        # ChatModel.objects.create(sender=chatDetails['sender'], receiver=chatDetails['receiver'], msg=chatDetails['msg'])
        obj = {}
        if file == '1':
            obj = ChatModel.objects.create(sender=chatDetails['sender'], receiver=chatDetails['receiver'], is_file=True, file=chatDetails['file'])
        else:
            obj = ChatModel.objects.create(sender=chatDetails['sender'], receiver=chatDetails['receiver'], is_file=False, text=chatDetails['text'])
        serialised = ChatSerializer(obj).data
        return serialised
    except Exception as e:
        print(str(e))
        return False

def fetch(details):
    try:
        print('fetch')
        data = ChatModel.objects.filter(
        Q(Q(sender=details['sender']) & Q(receiver=details['receiver'])) | 
        Q(Q(sender=details['receiver']) & Q(receiver=details['sender']))
        ).order_by('timestamp')
        # print(data)

        serialized_data = ChatSerializer(data, many=True)
        return serialized_data.data
    except Exception as e:
        print(str(e))
        return "error"

    
