from django.db import IntegrityError
from django.shortcuts import render,get_object_or_404,HttpResponseRedirect
from django.utils import timezone
from django.urls import reverse
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import JsonResponse
import json
from django.views import View
from django.template.loader import get_template
from django.core.mail import EmailMultiAlternatives
from django.core.mail import send_mail
from django.conf import settings

from . models import Usuarios
from . models import Conversaciones
from . models import Participantes
from . models import Chats
from . models import VerificacionCuentas

from django.core.files.storage import FileSystemStorage

import os
import random
from . variables import DIR_HOST_S
def home(request):
    
    error=False
    return render(request, 'ingreso.html',{
        'error':error,
        'DIR_HOST_S':DIR_HOST_S
    })

def room(request, room_name):
    return render(request, 'chatroom.html', {
        'room_name': room_name
    })

@login_required
def miperfil(request):
    id_activo=request.user.username
    datos_usuario=get_object_or_404(Usuarios,user_name=id_activo)
    fechacorta = datos_usuario.fecha_nacimiento.strftime('%Y-%m-%d')
    nombreusuario=datos_usuario.user_name[1:len(datos_usuario.user_name)]
    nombrecompleto=str(datos_usuario.nombre_usuario)
    if str(datos_usuario.sexo.lower())=='m':
        sexo=True
    else:
        sexo=False
    
    if request.method=='GET':
        return render(request, 'misdatosv2.html',{
            "datos_usuario":datos_usuario,    
            "fechacorta":fechacorta,
            "nombreusuario":nombreusuario,
            "nombrecompleto":nombrecompleto,
            "sexo":sexo,
            'DIR_HOST_S':DIR_HOST_S
        })
    else:
    
        usuario_reg=get_object_or_404(Usuarios,user_name=id_activo)
        perfil=get_object_or_404(Usuarios,user_name=id_activo)
        nombre=request.POST["nombre"]
        apellido=request.POST["apellido"]
        nacimiento=request.POST["nacimiento"]
        sexo_post=str(request.POST["sexo"])
        if str(sexo_post.lower())=='masculino':
            sexoreg='M'
        else:
            sexoreg='F'
        
        if len(request.FILES) >0 :
            perfil.image=request.FILES['inputfoto']

        perfil.nombre_usuario=nombre
        perfil.apellido_usuario=apellido
        perfil.fecha_nacimiento=nacimiento
        perfil.sexo=sexoreg
        perfil.save()
        
        return HttpResponseRedirect(reverse("mensajes:usuario",args=(usuario_reg.user_name,)))
        
@login_required
def usuario(request,logeado):
    id_activo=request.user.username
    logeado=request.user.username
    try:
        usuarios=get_object_or_404(Usuarios,user_name=id_activo)
        return render(request, 'usuario.html',{
            "usuarios":usuarios,
            'room_name': 'usuario',
            'logeado':logeado,
            'DIR_HOST_S':DIR_HOST_S
            
        })
    except IntegrityError:
        return render(request, 'home.html')
    
def enviar(user):
    datos=VerificacionCuentas.objects.get(user_name=user)
    codigo=datos.codigo_identificacion
    mail=datos.correo
    datousuario=Usuarios.objects.get(user_name=user)
    context={'mail':datos.correo ,
            'Nombre':(f"{datousuario.nombre_usuario}, {datousuario.apellido_usuario}") ,
            'user_name':datos.user_name,
            'codigo':codigo}
    template=get_template('autenticacion.html')
    content=template.render(context)

    email=EmailMultiAlternatives(
        'Correo para autenticacion',
        'MensajeriaApp',
        'mensajeriaapp86@gmail.com',
        [mail]
    )
    email.attach_alternative(content,'text/html')
    email.send()

def generarcodigoautenticacion(request,usuarioenvio):
    VerificacionCuentas.generarverificacion(usuarioenvio)
    enviar(usuarioenvio)
    return HttpResponseRedirect(reverse("mensajes:enviocorreo",args=(usuarioenvio,)))

def enviocorreo(request,usuarioenvio):
    datosverificacion=VerificacionCuentas.objects.get(user_name=usuarioenvio)
    if request.method=='GET':
        
        context={'mail':datosverificacion.correo ,
                'user_name':datosverificacion.user_name,
                }
        return render(request, 'enviocorreo.html',context) 
    else:
        codigover=request.POST["codigovalidacion"]
        if int(codigover)==datosverificacion.codigo_identificacion:
            
            datosverificacion.autenticado=True
            datosverificacion.fecha_autenticacion=timezone.now()
            datosverificacion.save()
            return HttpResponseRedirect(reverse("mensajes:usuario",args=(usuarioenvio,)))
        else:
            return HttpResponseRedirect(reverse("mensajes:enviocorreo",args=(usuarioenvio,)))
        
def signin(request):
    
    if request.method=='GET':
        error=False
        
        return render(request, 'ingreso.html',{
            'error':error,
            'DIR_HOST_S':DIR_HOST_S
        })
    else:
        datoingreso=request.POST['user']
        complemento=datoingreso[0:1]

        if complemento != '@':
            u=Usuarios.objects.values().filter(correo =datoingreso)
            if len(u)>0:
                usuario_ingreso=u[0]['user_name']
            else:
                usuario_ingreso=datoingreso

            
        else:
            usuario_ingreso=datoingreso

        listado=Usuarios.objects.values().filter(user_name__iexact=usuario_ingreso)
        if len(listado)>0:
            usuariobd=listado[0]['user_name']
        else:
            usuariobd=usuario_ingreso

        
        user = authenticate(
            request, username=usuariobd, password=request.POST['password']

            )
        if user is None:
            error=True
            return render(request, 'ingreso.html',{
                            'error':error,
                            'DIR_HOST_S':DIR_HOST_S}
                        )

        login(request, user)
        verificacion=VerificacionCuentas.control_verificacion(user)
        usuario_reg=get_object_or_404(Usuarios,user_name=user)
        if verificacion==0:
            
            ult_conexion=get_object_or_404(Usuarios,user_name=user)
            ult_conexion.ultima_conexion=timezone.now()
            ult_conexion.save()
            return HttpResponseRedirect(reverse("mensajes:usuario",args=(usuario_reg.user_name,)))
        else:
            if verificacion > 1:
                enviar(user)    
            return HttpResponseRedirect(reverse("mensajes:enviocorreo",args=(usuario_reg.user_name,)))
        
@login_required
def signout(request):
    logout(request)
    # return render(request, 'registrousuario.html')
    return HttpResponseRedirect(reverse("mensajes:home"))
        
def registro_usuario(request):
    errorusuario=False
    mensajeusuarioexiste=""
    errorcontrasena=False
    mensajecontrasena=""
    if request.method=='GET':
        return render(request, 'registrousuario.html',{
            'errorusuario':errorusuario,
            'mensajeusuarioexiste':mensajeusuarioexiste,
            'mensajecontrasena':errorcontrasena,
            'mensajecontraseña':mensajecontrasena
        }
        )
    else: 
        nombre=request.POST["nombre"]
        apellido=request.POST["apellido"]
        nacimiento=request.POST["nacimiento"]
        dato_sexo=request.POST["sexo"]
        if dato_sexo.lower=='masculino':
            sexo='M'
        else:
            sexo='F'
        nombre_usuario=request.POST["user"]
        complemento=nombre_usuario[0:1]

        if complemento != '@':
            nombre_usuario='@' + nombre_usuario
        
        email=request.POST["correo"]
        contrasena1=request.POST["contrasena1"]
        contrasena2=request.POST["contrasena2"]
        control=Usuarios.objects.values().filter(user_name__iexact=nombre_usuario)

        if len(control)>0:
            errorcontrasena=False
            mensajecontrasena=""
            errorusuario=True
            mensajeusuarioexiste=(f"El usuario {nombre_usuario} ya existe!")
            return render(request, 'registrousuario.html',{
                                    'errorusuario':errorusuario,
                                    'mensajeusuarioexiste':mensajeusuarioexiste,
                                    'errorcontrasena':errorcontrasena,
                                    'mensajecontrasena':mensajecontrasena
                                }
                            )
        if contrasena1==contrasena2:
            try:
                u=Usuarios(
                    nombre_usuario=nombre,
                    apellido_usuario=apellido,
                    fecha_nacimiento=nacimiento,
                    sexo=sexo,
                    user_name=nombre_usuario,
                    correo=email,
                    activo=True,
                    ultima_conexion=timezone.now(),
                    fecha_registro=timezone.now()
                )
                u.save()
                user = User.objects.create_user(nombre_usuario, password=contrasena1)
                user.save()
                login(request, user)
                usuario_reg=get_object_or_404(Usuarios,user_name=user)
                VerificacionCuentas.control_verificacion(nombre_usuario)
                enviar(nombre_usuario)    
                return HttpResponseRedirect(reverse("mensajes:enviocorreo",args=(nombre_usuario,)))

            except IntegrityError:
                errorcontrasena=False
                mensajecontrasena=""
                errorusuario=True
                mensajeusuarioexiste=(f"El usuario {nombre_usuario} ya existe!")
                return render(request, 'registrousuario.html',{
                                    'errorusuario':errorusuario,
                                    'mensajeusuarioexiste':mensajeusuarioexiste,
                                    'errorcontrasena':errorcontrasena,
                                    'mensajecontrasena':mensajecontrasena
                                }
                            )
        else:
            errorcontrasena=True
            mensajecontrasena="Las contraseñas no coinciden!"
            errorusuario=False
            mensajeusuarioexiste=""
            return render(request, 'registrousuario.html',{
                                    'errorusuario':errorusuario,
                                    'mensajeusuarioexiste':mensajeusuarioexiste,
                                    'errorcontrasena':errorcontrasena,
                                    'mensajecontrasena':mensajecontrasena
                                }
                            )

@login_required()
def registro_chat(request):
    if request.method=='GET':
        return render(request, 'nuevo_mensaje.html')
    else:
        id_activo=request.user.username
        destino=request.POST['destinatario']
        mensaje=request.POST['mensaje']
        Chats.registrochat(id_activo,destino,mensaje)
        return HttpResponseRedirect(reverse("mensajes:usuario",args=(id_activo,)))

@login_required()
def registrorapido(request,remitente,destino,textomensaje):
    id_activo=remitente
    destino=destino
    mensaje=textomensaje
    Chats.registrochat(id_activo,destino,mensaje)
    return HttpResponseRedirect(reverse("mensajes:usuario"))
        
@login_required
def listadousuarios(request):
    id_activo=request.user.username
    datos=Usuarios.listado_usuarios(id_activo)
    return JsonResponse(datos,safe=False)

@login_required
def datosperfil(request,usuariodestino):
    id_activo=request.user.username
    #datos=Usuarios.listado_usuarios(id_activo)
    datos=Chats.resumenchat(id_activo,usuariodestino)
    return JsonResponse(datos,safe=False)

@login_required
def mismensajes(request):
    id_activo=request.user.username
    datos=Usuarios.listado_converacion(id_activo)
    return JsonResponse(datos,safe=False)

@login_required
def listadochat(request,remitente):
    id_activo=request.user.username
    datos=Usuarios.listado_chat(id_activo,remitente)
    return JsonResponse(datos,safe=False)

@login_required
def datosconexiones(request,destino):
    
    u=Usuarios.objects.values().filter(user_name=destino)
    ultima=u[0]['ultima_conexion'].strftime('%d/%m/%y %H:%M')
    fotoperfil=u[0]['image']
    original=list()
    original.append(  dict([('conexiones',  
                                dict([('ultima_conexion',ultima),('fotoperfil',fotoperfil)   
                                ]) 
                            )])
                    )

    return JsonResponse(original,safe=False)


def validaciones(request,usuariodestino):
    control=Usuarios.objects.values().filter(user_name__iexact=usuariodestino)
    if len(control)>0:    
        errorusuario=True
        mensajeusuarioexiste=(f"El usuario {usuariodestino} ya existe!")
    else:
        errorusuario=False
        mensajeusuarioexiste=""
    
    original=list()
    original.append(  dict([('validacion',  
                                dict([('Existe',errorusuario),('mensaje',mensajeusuarioexiste)   
                                ]) 
                            )])
                    )

    return JsonResponse(original,safe=False)

@login_required()
def resumen(request,usuariodestino):
    id_activo=request.user.username
    datos=Chats.resumenchat(id_activo,usuariodestino)
    enviados=datos[0]
    nombreusuario=datos[0]['suusuario'][1:len(datos[0]['suusuario'])]
    
    return render(request, 'resumen.html',{
            "enviados":enviados,    
            "nombreusuario":nombreusuario,
            'DIR_HOST_S':DIR_HOST_S
        })

@login_required()
def eliminarconversacion(request,usuariodestino):
    id_activo=request.user.username
    conver_reg=Conversaciones.obtenerconversacion(id_activo,usuariodestino)
    Chats.eliminar_conversacion(conver_reg)
    
    return HttpResponseRedirect(reverse("mensajes:resumen",args=(usuariodestino,)))

@login_required()
def eliminarperfil(request):
    id_activo=request.user.username
    datos=Usuarios.resumen_cuenta(id_activo)
    datos_usuario=datos[0]
    # nombreusuario=datos[0]['suusuario'][1:len(datos[0]['suusuario'])]
    
    # return render(request, 'resumen.html',{
    #         "enviados":enviados,    
    #         "nombreusuario":nombreusuario
    #     })
    usuario=get_object_or_404(Usuarios,user_name=id_activo)
    fechacorta = usuario.fecha_nacimiento.strftime('%Y-%m-%d')
    nombreusuario=usuario.user_name[1:len(usuario.user_name)]
    nombrecompleto=str(usuario.nombre_usuario)
    if str(usuario.sexo.lower())=='m':
        sexo=True
    else:
        sexo=False
    
    if request.method=='GET':
        return render(request, 'eliminarperfil.html',{
            "datos_usuario":datos_usuario,    
            "fechacorta":fechacorta,
            "nombreusuario":nombreusuario,
            "nombrecompleto":nombrecompleto,
            "sexo":sexo
        })
    else:
        accion=Usuarios.eliminar_perfil(id_activo)
        if accion:
            return HttpResponseRedirect(reverse("mensajes:home"))
        else:
            return render(request, 'eliminarperfil.html',{
                "datos_usuario":datos_usuario,    
                "fechacorta":fechacorta,
                "nombreusuario":nombreusuario,
                "nombrecompleto":nombrecompleto,
                "sexo":sexo
            })
        