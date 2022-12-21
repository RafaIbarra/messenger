import {DIR_HOST} from './variables.js'
export function ultimaconexion(conusuario){
    const urlconex = DIR_HOST+'/mensajes/datosconexiones/' + conusuario+'/';
    var div = document.getElementById('id_conexion');
    fetch(urlconex)
    .then((resp) => resp.json())
    .then(function(data) {
      let authors = data;
      
      return authors.forEach((e) => {    //< ---  recorremos data
        div.innerHTML=e.conexiones.ultima_conexion; 
    
    });

  })

}