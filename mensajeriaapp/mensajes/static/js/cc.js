
import {cargaconversaciones} from './cargaconversaciones.js'
import {DIR_HOST} from './variables.js'

export function carganoversacion(sesion,insertarmensaje,tiempo){
  
  if (sesion.length >0){
    
    let idfoto="cabecera_foto_perfil"
    let foto = document.getElementById(idfoto).src;
    
    foto=foto.replace(DIR_HOST+"/mensajes/media/", "");
    

    var datosperfil=[];
    
  
    const url_usuario = DIR_HOST+'/mensajes/datosperfil/' + sesion;
    
    fetch(url_usuario)
    .then((resp) => resp.json())
    .then(function(data) {
      let authors = data;
  
      datosperfil = data;
      return authors.forEach((e) => {    
      
        cargaconversaciones('unico',sesion,insertarmensaje,tiempo,e.sufoto)

    
    });

   })
          

  } else {
    
    
    const url = DIR_HOST+'/mensajes/mismensajes/';
    
    const cards = document.getElementById("tarjeta");
    var div = document.getElementById('conversaciones');
    

    fetch(url)
    .then((resp) => resp.json())
    .then(function(data) {
      let authors = data;
      
      return authors.forEach((e) => {    
        cargaconversaciones('todos',e.mesajes.con, e.mesajes.mensaje, e.mesajes.fechacorta,e.mesajes.fotoperfil)

    
    });

  })

  }
  
  
};

