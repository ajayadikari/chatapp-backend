from adrf.decorators import api_view
import json
from asgiref.sync import sync_to_async
from .customMethods import store, fetch
from rest_framework.response import Response
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated


@api_view(['POST'])
@permission_classes([IsAuthenticated])
async def storeMsg(request, file):
    chatDetails = {}
    if(file=='1'):
        sentfile = request.FILES.get('file')
        chatDetails = {
            'sender': request.POST.get('sender'), 
            "receiver": request.POST.get('receiver'), 
            "file": sentfile
        }
        
        # print(sentfile)
    else:
        chatDetails = {
            'sender': request.POST.get('sender'), 
            "receiver": request.POST.get('receiver'), 
            "text": request.POST.get('text')
        }
        # print(chatDetails)
    try:
        obj = await sync_to_async(store)(chatDetails, file)
        return Response({
            'success': True, 
            'msg': 'chat stored successfully', 
            "data": obj
        })
    except Exception as e:
        return Response({
            'success': False, 
            'msg': 'unable to store chat', 
            "error": str(e)
        })

# client will send the 2 usernames, whose chat needed to be fetched
@api_view(['GET'])
@permission_classes([IsAuthenticated])
async def fetchChat(request, sender, receiver):
    try:
        details = {
            "sender": sender, 
            "receiver": receiver
        }
        data = await sync_to_async(fetch)(details)

        return Response({
            "success": True,
            "data": data
        })

    except Exception as e:
        return Response({
            "success": False,
            "msg": "unable to fetch the previous chat", 
            "error": e
        })