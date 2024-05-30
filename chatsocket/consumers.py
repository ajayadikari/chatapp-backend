from channels.consumer import AsyncConsumer, SyncConsumer
from channels.exceptions import StopConsumer
from asgiref.sync import sync_to_async
from .customMethods import CustomMethods
from channels.layers import get_channel_layer
import json


class MyAsyncConsumer(AsyncConsumer):

    async def websocket_connect(self, event):
        username = self.scope['url_route']['kwargs']['username']
        print(username)
        channel_name = self.channel_name
        channel_layer = self.channel_layer

        await sync_to_async(CustomMethods.set_channel)(username, channel_name)

        print("username of the client: ",username)
        try:
            await self.send({
                'type': 'websocket.accept'
            })
        except Exception as e:
            print(str(e))

    async def websocket_receive(self, event):
        message = json.loads(event['text'])
        # print(message)
        receivercn = message['receivercn']
        channel_layer = self.channel_layer
        obj = {
            "msg": message['msg'], 
            "is_file": message['file']
        }
        

        try:
            await channel_layer.send(receivercn, {
                "type": "channel.message", 
                "data": json.dumps(obj), 
                "is_File": message['file'] 
            })
        except Exception as e:
            print(str(e))
        

    async def websocket_disconnect(self, event):
        print("disconnect")
        raise StopConsumer
    

    async def channel_message(self, event):
        message = json.loads(event['data'])
        obj = json.dumps({
            "msg": message['msg'], 
            "is_file": message['is_file']
        })
        try:
            await self.send({
                'type': 'websocket.send',
                'text': obj 
            })
        except Exception as e:
            print("error while sending to receiver")
            print(str(e))
    
    
    
