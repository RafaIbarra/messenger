from django.db import models
from django.db.models import Q
from django.utils import timezone
import os
from pathlib import Path
import random
from django.db.transaction import TransactionManagementError
from django.db import DatabaseError, transaction
from django.contrib.auth.models import User
# from django.contrib.auth.models import User
# from channels.db import database_sync_to_async
# import pandas as pd
# import numpy as np
# from django.core.serializers import serialize
# from django.http import JsonResponse
# import json


def create_path(instance, filename):
    return os.path.join(
        instance.user_name 
        + Path(filename).suffix
    )

class VerificacionCuentas(models.Model):
    user_name=models.CharField(max_length=100,blank=False,unique=True)
    correo=models.EmailField()
    codigo_identificacion=models.BigIntegerField(default=0,blank=False)
    fecha_envio=models.DateTimeField("fecha envio")
    autenticado=models.BooleanField(default=False)
    fecha_autenticacion=models.DateTimeField("fecha autenticacion",blank=True,null=True)

    class Meta:
        db_table="VerificacionCuentas"

    def control_verificacion(usuario):
        verificacion=VerificacionCuentas.objects.values().filter(user_name=usuario)
        if len(verificacion)==0:
           VerificacionCuentas.generarverificacion(usuario)
           generado=VerificacionCuentas.objects.values().filter(user_name=usuario)
           respuesta=generado[0]['codigo_identificacion']

        else:
            if verificacion[0]['autenticado']:
                respuesta=0 # si ya cuenta con la identificacion
            else:
                respuesta=1 # si se envio el correo pero aun no cargo el codigo


        return respuesta

    def generarverificacion(usuario):
        datos=Usuarios.objects.get(user_name=usuario)
        codigo=random.randint(100000,999999)
        verificacion=VerificacionCuentas.objects.values().filter(user_name=usuario)
        if len(verificacion)>0: 
            eliminar=VerificacionCuentas.objects.get(user_name=usuario)
            eliminar.delete()

        ver=VerificacionCuentas(
                user_name=usuario,
                correo=datos.correo,
                codigo_identificacion=codigo,
                fecha_envio=timezone.now(),
                autenticado=False
            )
        ver.save()
        respuesta=codigo
        return respuesta


class Usuarios(models.Model):
    nombre_usuario=models.CharField(max_length=200,blank=False)
    apellido_usuario=models.CharField(max_length=200,blank=False)
    fecha_nacimiento=models.DateField("Fecha Nacimiento")
    sexo=models.CharField(max_length=1,blank=False,default="M")
    user_name=models.CharField(max_length=100,blank=False,unique=True)
    correo=models.EmailField()
    activo=models.BooleanField(default=False)
    ultima_conexion=models.DateTimeField("fecha ultma conexion")
    fecha_registro=models.DateTimeField("fecha registro")
    image=models.ImageField(default='sinperfil.png',blank=True,upload_to=create_path)

    class Meta:
        db_table="Usuarios"
        
       

    def __str__(self):
        return (f"{self.nombre_usuario.capitalize()} , {self.apellido_usuario.capitalize()}")


    def listado_converacion(usuario_activo):
        listado=Conversaciones.objects.values().filter(Q(destinatario=usuario_activo)|Q(remitente=usuario_activo))
        original=list()
        for i in listado:
            ult=Chats.ultimo_chat(i["id"])
            fechacorta = ult[0]['fecha_registro'].strftime('%d/%m/%y %H:%M')
            
            if i["remitente"]!=usuario_activo:
                imagenperfil=Usuarios.objects.values().filter(user_name=i['remitente'])    
                original.append(  dict([('mesajes',  dict([('id',i['id']), ('con',i['remitente']), ('mensaje',ult[0]['mensaje']), ('Fecha',ult[0]['fecha_registro'])
                                , ('id_mensaje',ult[0]['id']), ('fechacorta',fechacorta), ('fotoperfil',imagenperfil[0]['image'])    ]) )])     )     
            else :
                imagenperfil=Usuarios.objects.values().filter(user_name=i['destinatario'])    
                original.append(  dict([('mesajes',  dict([('id',i['id']), ('con',i['destinatario']), ('mensaje',ult[0]['mensaje']), ('Fecha',ult[0]['fecha_registro'])
                , ('id_mensaje',ult[0]['id']), ('fechacorta',fechacorta), ('fotoperfil',imagenperfil[0]['image'])       ]) )])     )     
        


        original.sort(key=lambda p: p['mesajes']['id_mensaje'],reverse=True)
        return original

    def resumen_cuenta(usuario_activo):
        dato_usuario=Usuarios.objects.values().filter(user_name=usuario_activo)
        
        id_usuario=dato_usuario[0]['id']
        cantenviado=0
        cantrecibo=0
        listado_conversaciones=Conversaciones.objects.values().filter(Q(destinatario=usuario_activo)|Q(remitente=usuario_activo))

        for i in listado_conversaciones:
            mensajes=Chats.objects.values().filter(id_conversacion_id=i['id'])

            for m in mensajes:
                if m['id_user_id']==id_usuario:
                    cantenviado=cantenviado + 1
                else:
                    cantrecibo=cantrecibo + 1

        original=list()

        original.append(   
                                    dict([  
                                        ('Cantidadconversaciones',len(listado_conversaciones)),
                                        ('cantenviado',cantenviado),
                                        ('cantrecibo',cantrecibo), 
                                        ('nombre_usuario',dato_usuario[0]['nombre_usuario'].strip()), 
                                        ('apellido_usuario',dato_usuario[0]['apellido_usuario'].strip()), 
                                        ('fecha_nacimiento',dato_usuario[0]['fecha_nacimiento'].strftime('%d/%m/%Y %H:%M:%S')), 
                                        ('sexo',dato_usuario[0]['sexo']), 
                                        ('user_name',dato_usuario[0]['user_name'].strip()), 
                                        ('correo',dato_usuario[0]['correo']), 
                                        ('ultima_conexion',dato_usuario[0]['ultima_conexion'].strftime('%d/%m/%Y %H:%M:%S')), 
                                        ('fecha_registro',dato_usuario[0]['fecha_registro'].strftime('%d/%m/%Y %H:%M:%S')), 
                                        ('image',dato_usuario[0]['image']), 




                                        ]) 
                                             
                        )
        return original

    def eliminar_perfil(usuario_del):
        respuesta=True
        listado_conversaciones=Conversaciones.objects.values().filter(Q(destinatario=usuario_del)|Q(remitente=usuario_del))
        for i in listado_conversaciones:
            try :
                del_conv=i['id']
                Chats.eliminar_conversacion(del_conv)

            except Exception as msg_error:
                respuesta=msg_error

        del_usu=Usuarios.objects.get(user_name=usuario_del)
        del_usu.delete()
        u=User.objects.get(username=usuario_del)
        u.delete()

        return respuesta

    def mis_datos(usuario):
        listado=Usuarios.objects.values().filter(user_name=usuario)
        return listado


    def listado_chat(usuario_activo,con_usuario):
        listado=Conversaciones.objects.values().filter(Q(destinatario=usuario_activo)|Q(remitente=usuario_activo)).filter(Q(destinatario=con_usuario)|Q(remitente=con_usuario))
        
        original=list()
        if len(listado) >0:
            cod=listado[0]['id']
            chat=Chats.objects.values().filter(id_conversacion=cod)
            
            
            for i in chat:
                envio=Usuarios.objects.get(id=i['id_user_id'])
                nombreenvio=envio.user_name
                imagen=Usuarios.objects.values().filter(id=i['id_user_id'])
                fotoperfil= imagen[0]['image']
                
                fechacorta = i['fecha_registro'].strftime('%d/%m/%y %H:%M')
                original.append(  dict([('chat',  dict([ ('id',i['id']), ('mensaje',i['mensaje']), ('leido',i['leido']), ('fecha',i['fecha_registro']), 
                ('id_user',i['id_user_id']), ('envio',nombreenvio), ('fechacorta',fechacorta), ('fotoperfil',fotoperfil),   ]) )])     )     

            original.sort(key=lambda p: p['chat']['id'])
        return original


    def listado_usuarios(usuario_activo):
        listado=Usuarios.objects.values().exclude(user_name=usuario_activo)
        original=list()
        for i in listado:
            
            original.append(  dict([('disponibles',  dict([ ('id',i['id']), ('user_name',i['user_name']), ('image',i['image'])   ]) )])     )     

        original.sort(key=lambda p: p['disponibles']['user_name'])
        return original

    
class Conversaciones(models.Model):
    remitente=models.CharField(max_length=200,blank=False)
    destinatario=models.CharField(max_length=200,blank=False)
    fecha_registro=models.DateTimeField("fecha registro")

    class Meta:
        db_table="Conversaciones"

    def obtenerconversacion(envio,recibio):
        a=Conversaciones.objects.filter(remitente=envio,destinatario=recibio)
        result=a.values_list('id')
        resul_list=list(result)
        if len(resul_list)==0:
            a_final=0
        else:
            final=list(resul_list[0])
            a_final=int(final[0])
        
        b=Conversaciones.objects.filter(remitente=recibio,destinatario=envio)
        result=b.values_list('id')
        resul_list=list(result)
        if len(resul_list)==0:
            b_final=0
        else:
            final=list(resul_list[0])
            b_final=int(final[0])

        resul_final=a_final + b_final
        return resul_final
    
    
class Participantes(models.Model):
    id_conversacion=models.ForeignKey(Conversaciones,on_delete=models.CASCADE,)
    id_user=models.ForeignKey(Usuarios,on_delete=models.CASCADE,)
    fecha_registro=models.DateTimeField("fecha registro")

    class Meta:
        db_table="Participantes"

    
class Chats(models.Model):
    id_conversacion=models.ForeignKey(Conversaciones,on_delete=models.CASCADE,)
    id_user=models.ForeignKey(Usuarios,on_delete=models.CASCADE,)
    mensaje=models.CharField(max_length=200,blank=False)
    leido=models.BooleanField(default=False)
    fecha_registro=models.DateTimeField("fecha registro")

    class Meta:
        db_table="Chats"

    

    def obtner_mensajes(id_conv):
        
        data=list(Chats.objects.values().filter(id_conversacion=id_conv))
        return data
    
    def ultimo_chat(id_conv):
        data=Chats.objects.values().filter(id_conversacion=id_conv).order_by('-id')[:1]
        return data


    def registrochat(origen,destino,chat_texto):

        conver_reg=Conversaciones.obtenerconversacion(origen,destino)
        participante1=origen
        participante2=destino
        #if conv1 is None and conv2 is None:
        if conver_reg==0: #crea una nueva conversacion
            m=Conversaciones(
                remitente=origen,
                destinatario=destino,
                fecha_registro=timezone.now()
            )
            m.save()
            part1=Participantes(
                                id_conversacion=Conversaciones.objects.get(remitente=participante1,destinatario=participante2),
                                id_user=Usuarios.objects.get(user_name=participante1),
                                fecha_registro=timezone.now()
                                )  
            part1.save()

            part2=Participantes(
                                id_conversacion=Conversaciones.objects.get(remitente=participante1,destinatario=participante2),
                                id_user=Usuarios.objects.get(user_name=participante2),
                                fecha_registro=timezone.now()
                                )
            part2.save()

            nueva_conversacion=Conversaciones.objects.get(remitente=participante1,destinatario=participante2)
            conver_reg=nueva_conversacion.id

        cht=Chats(
                id_conversacion=Conversaciones.objects.get(pk=conver_reg),
                id_user=Usuarios.objects.get(user_name=participante1),
                mensaje=chat_texto,
                leido=False,
                fecha_registro=timezone.now()

                )
        cht.save()

    def resumenchat(solicita,destino):
        conver_reg=Conversaciones.obtenerconversacion(solicita,destino)
        id_solicita=Usuarios.objects.values().filter(user_name=solicita)
        id_destino=Usuarios.objects.values().filter(user_name=destino)
        
        original=list()
        
        if conver_reg==0:
            mis_mensajes=list()
            sus_mensajes=list()
        else:
            mis_mensajes=Chats.objects.values().filter(Q(id_conversacion_id=conver_reg) & Q(id_user_id=id_solicita[0]['id'])).order_by('-id')
            sus_mensajes=Chats.objects.values().filter(Q(id_conversacion_id=conver_reg) & Q(id_user_id=id_destino[0]['id'])).order_by('-id')


        if len(mis_mensajes)>0:
            miultimomensaje=mis_mensajes[0]['fecha_registro'].strftime('%d/%m/%y %H:%M')
        else:
            miultimomensaje='--/--/-- 00:00'
        


        if len(sus_mensajes)>0:
            suultimomensaje=sus_mensajes[0]['fecha_registro'].strftime('%d/%m/%y %H:%M')
        else:
            suultimomensaje='--/--/-- 00:00'

        
        
        original.append(  dict([    ('mifoto',id_solicita[0]['image'] ),
                                    ('cantidadEnviada',len(mis_mensajes) ), 
                                    ('miultimomensaje',miultimomensaje ), 
                                    ('miusuario',solicita ), 

                                    ('sufoto',id_destino[0]['image'] ),
                                    ('cantidadRecibido',len(sus_mensajes) ),
                                    ('sultimomensaje',suultimomensaje ),
                                    ('suusuario',destino ), 
                                    ('Nombre',id_destino[0]['nombre_usuario'] ), 
                                    ('Apellido',id_destino[0]['apellido_usuario'] ), 

                                    ('total',len(sus_mensajes) + len(mis_mensajes) ),

                            ])      ) 

        resultado=original
        

        return resultado

    def eliminar_conversacion(conversacion):
        respuesta=True
        try :
            chat=Chats.objects.all().filter(id_conversacion_id=conversacion)
            chat.delete()
            part=Participantes.objects.all().filter(id_conversacion_id=conversacion)
            part.delete()
            conver=Conversaciones.objects.all().filter(id=conversacion)
            conver.delete()

        except Exception as msg_error:
            respuesta=msg_error

        return respuesta
            



