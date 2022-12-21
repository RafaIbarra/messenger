# from channels.auth import AuthMiddlewareStack
# from channels.routing import ProtocolTypeRouter,URLRouter
# from channels.security.websocket import AllowedHostsOriginValidator
# import mensajes.routing

# application = ProtocolTypeRouter({
#     'websocket': AllowedHostsOriginValidator( AuthMiddlewareStack(
#         URLRouter(
#             mensajes.routing.websocket_urlpatterns
#         )
#     )
#     ),
# })