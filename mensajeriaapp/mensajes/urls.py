from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static


app_name="mensajes"
urlpatterns = [
    path('', views.home, name='home'),

    path("registrousuario/",views.registro_usuario,name="registro_usuario"),
    path("usuario/<str:logeado>/",views.usuario,name="usuario"),
    path("miperfil/",views.miperfil,name="miperfil"),
    path("signin/",views.signin,name="signin"),
    path("signout/",views.signout,name="signout"),
    path("registroconversacion/",views.registro_chat,name="registro_conversacion"),
    path("registrorapido/<str:remitente>/<str:destino>/<str:textomensaje>/",views.registrorapido,name="registrorapido"),
    path("mismensajes/",views.mismensajes,name="mismensajes"),
    path("chats/<str:remitente>/",views.listadochat,name="listadochat"),
    path("datosconexiones/<str:destino>/",views.datosconexiones,name="datosconexiones"),
    path("enviocorreo/<str:usuarioenvio>/",views.enviocorreo,name="enviocorreo"),
    path("generarcodigo/<str:usuarioenvio>/",views.generarcodigoautenticacion,name="generarcodigo"),
    path("listadousuarios/",views.listadousuarios,name="listadousuarios"),
    path("resumen/<str:usuariodestino>/",views.resumen,name="resumen"),
    path("datosperfil/<str:usuariodestino>/",views.datosperfil,name="datosperfil"),
    path("validaciones/<str:usuariodestino>/",views.validaciones,name="validaciones"),
    path("eliminarconversacion/<str:usuariodestino>/",views.eliminarconversacion,name="eliminarconversacion"),
    path("eliminarperfil/",views.eliminarperfil,name="eliminarperfil"),


]  

#if settings.DEBUG:
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)