import json
from channels.generic.websocket import AsyncWebsocketConsumer
from . models import Chats,Conversaciones,Usuarios
from channels.db import database_sync_to_async
from django.utils import timezone
from django.contrib.auth.models import User
from django.http import JsonResponse



class ChatRoomConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.logeado = self.scope['url_route']['kwargs']['logeado']
        
        self.room_name = 'usuario'
        self.room_group_name =  self.room_name

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        remitente = text_data_json['remitente']
        destinatario = text_data_json['destinatario']
        fechahora= text_data_json['fechahora']
        logeado= text_data_json['logeado']
        accion= text_data_json['accion']
        

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chatroom_message',
                'message': message,
                'remitente': remitente,
                'destinatario': destinatario,
                'fechahora':fechahora,
                'logeado':logeado,
                'accion':accion,
                
            },
            
        )

    async def chatroom_message(self, event):
        
        message = event['message']
        remitente = event['remitente']
        destinatario = event['destinatario']
        fechahora = event['fechahora']
        logeado = event['logeado']
        accion = event['accion']
        
        if accion=='enviomensaje':
            if self.logeado==remitente:
                await registro(message,remitente,destinatario)

        
        
        await self.send(text_data=json.dumps({'message': message,
                                            'remitente': remitente,
                                            'destinatario':destinatario,
                                            'fechahora':fechahora,
                                            'logeado':logeado,
                                            'accion':accion
                                            })
                        )
        
@database_sync_to_async
def registro(mensajeenviado,envia,recibe):
    
    
    a=Conversaciones.obtenerconversacion(envia,recibe)
    if a==0:
        Chats.registrochat(envia,recibe,mensajeenviado)
    else:
        key_query=Chats(
                        id_conversacion=Conversaciones.objects.get(pk=a),
                        id_user=Usuarios.objects.get(user_name=envia),
                        mensaje=mensajeenviado,
                        leido=False,
                        fecha_registro=timezone.now())
        key_query.active_connections =1
        key_query.save()





