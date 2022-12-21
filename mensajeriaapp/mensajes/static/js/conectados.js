import {DIR_HOST} from './variables.js'
export function cargar_conectados(conusuario,tiempo){
    
    let origen=tiempo;
    if (tiempo=='En Linea'){
        tiempo='Conectado.';

    }else{
        tiempo=tiempo.toString().slice(-5);
    }
    let carga_dato=new String;
    carga_dato='no';
    let div1 = document.getElementById("conectados");
    
    let id_spam_conectado=conusuario+'_span_conectado'
    let id_separador=conusuario+'br_conectado';
    let conusuario_conectado=conusuario +'_conectado'
    let contenedor_usuario=conusuario +'_contenedor'
        
    var div = document.getElementById(contenedor_usuario);

    if(div !== null){
        
        let control_tiempo_actual=document.getElementById(id_spam_conectado).innerText;

        if(control_tiempo_actual.length==0){
            control_tiempo_actual='Conectado.';
        }

        if (control_tiempo_actual !==tiempo){
            var parent = div.parentElement;
            parent.removeChild(div);
            div.remove();
            carga_dato='si';    
        }
        
    } else {
        carga_dato='si';
    }

    if (carga_dato=='si'){
        let contenedor= document.createElement("div");
        contenedor.setAttribute("class","contenedoractivo");
        contenedor.setAttribute("id", contenedor_usuario);
        

        let principal_conectado = document.createElement("div");
        principal_conectado.setAttribute("class","friend-drawer friend-drawer--onhover")
        principal_conectado.setAttribute("id", conusuario_conectado);


        let elemento_img_conectado=document.createElement("img");
        const urlconcetado = DIR_HOST +'/mensajes/datosconexiones/'+conusuario;

        fetch(urlconcetado)
        .then((resp) => resp.json())
        .then(function(data) {
          let authors = data;
          
          return authors.forEach((e) => {    
            
            elemento_img_conectado.setAttribute("class","profile-image-conectados")
            elemento_img_conectado.setAttribute("src",DIR_HOST+"/mensajes/media/"  +e.conexiones.fotoperfil)
            elemento_img_conectado.setAttribute("alt","")
    
        
        });
    
        })
        

        let secundario_conectado = document.createElement("div");
        secundario_conectado.setAttribute("class","text")

        let elemntoh6_conectado=document.createElement("h6");
        elemntoh6_conectado.innerHTML = conusuario;

        let elemto_span_conectado=document.createElement("span");
        elemto_span_conectado.setAttribute("id",id_spam_conectado)
        
        if (origen=='En Linea'){
            elemto_span_conectado.setAttribute("class","punto")
            
        }else {
            elemto_span_conectado.setAttribute("class","time text-muted small")
            elemto_span_conectado.innerHTML=tiempo;
        }

    
        secundario_conectado.appendChild(elemntoh6_conectado);
        principal_conectado.appendChild(elemento_img_conectado);
        principal_conectado.appendChild(secundario_conectado);
        principal_conectado.appendChild(elemto_span_conectado);

        
        contenedor.appendChild(principal_conectado);
        div1.appendChild(contenedor);
      
        
    }
    
    

    
    

}