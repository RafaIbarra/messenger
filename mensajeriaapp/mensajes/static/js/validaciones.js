import {DIR_HOST} from './variables.js'

document.querySelector('#user').onblur = function (e) {
        
    let elementuser=document.getElementById('user');
    
    let valor=elementuser.value;
    var primeraletra=valor.charAt(0);
    if (primeraletra !=='@'){
        valor='@' + valor
    }
    
    let control=DIR_HOST+'/mensajes/validaciones/'+valor;

    let elementomensaje=document.getElementById('mensajeuserfijo');
    fetch(control)
    .then((resp) => resp.json())
    .then(function(data) {
      let authors = data;
      
      return authors.forEach((e) => {    
        
        if(e.validacion.Existe){
            
            elementomensaje.innerHTML=e.validacion.mensaje
            elementomensaje.style.display ="inline-block"

        }else{
            elementomensaje.innerHTML=""
            elementomensaje.style.display ="none"
        }

    
    });

  })
    
}


