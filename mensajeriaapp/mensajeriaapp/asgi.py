"""
ASGI config for mensajeriaapp project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/howto/deployment/asgi/
"""

import os
from django.core.asgi import get_asgi_application

from channels.routing import ProtocolTypeRouter,URLRouter
from channels.auth import AuthMiddlewareStack
from channels.security.websocket import AllowedHostsOriginValidator
from django.urls import path
from mensajes.consumers import ChatRoomConsumer
from django.urls import re_path


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mensajeriaapp.settings')

#application = get_asgi_application()

mensajeriaapp = get_asgi_application()
application=ProtocolTypeRouter({
    "http": mensajeriaapp,
    # WebSocket chat handler
    "websocket": AllowedHostsOriginValidator(
        AuthMiddlewareStack(
            URLRouter([
                #path(r'ws/chat/(?P<room_name>\w+)/$', ChatRoomConsumer.as_asgi()),
                #path("ws/chat/room/", ChatRoomConsumer.as_asgi()),
                path("ws/mensajes/usuario/<str:logeado>/", ChatRoomConsumer.as_asgi()),
                
                #re_path(r'ws/mensajes/usuario/(?P<logeado>\w+)/$', ChatRoomConsumer),

                
            ])
        )
    ),


}

)

