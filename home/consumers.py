# chat/consumers.py
import json
from channels.generic.websocket import WebsocketConsumer

import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from home.models import Comment, Task, Share
from account.models import CustomUser
class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name

        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )

        self.accept()

    def disconnect(self, close_code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        action = text_data_json['action']
        print(action)
        if action == 'message':
            message = text_data_json['message']
            user_id = text_data_json['user_id']
            task_id = text_data_json['task_id']
            user = CustomUser.objects.filter(id=user_id).first()
            task = Task.objects.filter(id=task_id).first()

            print(user)
            print(task.user)
            if Share.objects.filter(user=user, task=task, status=2) and user != task.user and user and task and message:
                comment = Comment(text=message,user=user,task=task)
                comment.save()
                print(comment.id)

                async_to_sync(self.channel_layer.group_send)(
                    self.room_group_name,
                    {
                        'type': 'chat_message',
                        'action':'message',
                        'message': message,
                        'message_id': comment.id,
                        'user_id': user_id,
                    }
                )
        elif action == 'delete':
            message_id = text_data_json['message_id']
            user_id = text_data_json['user_id']
            task_id = text_data_json['task_id']
            
            if message_id and user_id:
                message = Comment.objects.filter(id=message_id).first()
                user = CustomUser.objects.filter(id=user_id).first()   
                task = Task.objects.filter(id=task_id).first()
                if (Share.objects.filter(user=user, task=task, status=2) and message.user == user) or task.user == user:
                    'DELETE'
                    message.delete()
                    data={
                        'type': 'chat_message',
                        'action':'delete',
                        'message_id': message_id
                    }

                    async_to_sync(self.channel_layer.group_send)(
                        self.room_group_name,
                        data,
                    )

        elif action == 'edit':
            message_id = text_data_json['message_id']
            user_id = text_data_json['user_id']
            task_id = text_data_json['task_id']

            new_message = text_data_json['message']
            
            if message_id and user_id and new_message:
                message = Comment.objects.filter(id=message_id).first()
                user = CustomUser.objects.filter(id=user_id).first()   
                task = Task.objects.filter(id=task_id).first()

                if Share.objects.filter(user=user, task=task, status=2) and message.user == user:
                    message.text=new_message
                    message.save()
                    data={
                        'type': 'chat_message',
                        'action':'edit',
                        'message_id': message_id,
                        'message':message.text,
                    }

                    async_to_sync(self.channel_layer.group_send)(
                        self.room_group_name,
                        data,
                    )

    # Receive message from room group
    def chat_message(self, event):
        data={}
        if 'action'in event:
            data['action']=event['action']
        if 'message_id' in event:
            data['message_id']=event['message_id']
        if 'message' in event:
            data['message']=event['message']
        if 'user_id' in event:
            data['user_id']=event['user_id']

        # Send message to WebSocket
        self.send(text_data=json.dumps(data))