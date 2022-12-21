import {cargadato} from './chats.js'
import {ultimaconexion} from './datosconexciones.js'
import {DIR_HOST} from './variables.js'
export function cargaconversaciones(tipo,conusuario,mensaje,tiempo,fotoperfil){
    let div1 = document.getElementById("conversaciones");
    
    let div3 = document.getElementById("Chatcabecera");
    

    let id_separador=conusuario+'br';
    
    
    if (mensaje.length >25){
        
        mensaje=mensaje.slice(-25)
        mensaje=mensaje + '. . . .'
    }
    
    if(tipo=='unico'){
        var div = document.getElementById(conusuario);
        var sep_elimininar = document.getElementById(id_separador);
        if(div !== null){
            div.remove();
            sep_elimininar.remove();
        }
        var theFirstChild = div1.firstChild;
        
        var hr_sep = document.getElementById(id_separador);
        
        if(hr_sep !== null){
            
            hr_sep.remove();
        }
    }

    
    let principal = document.createElement("div");
    principal.setAttribute("class","friend-drawer friend-drawer--onhover")

    let elemento_img=document.createElement("img");
    elemento_img.setAttribute("class","profile-image")
    
    elemento_img.setAttribute("src",DIR_HOST +"/mensajes/media/"  +fotoperfil)
    

    let idfotoperfil="fotoperfil" +conusuario
    elemento_img.setAttribute("alt","")
    elemento_img.setAttribute("id",idfotoperfil)

    let secundario = document.createElement("div");
    secundario.setAttribute("class","text")

    let elemntoh6=document.createElement("h6");

    let elemento_p=document.createElement("p");
    elemento_p.setAttribute("class","text-muted")

    let elemto_span=document.createElement("span");
    elemto_span.setAttribute("class","time text-muted small")

    let sep= document.createElement("hr");
    sep.setAttribute("id", id_separador);

    elemento_p.innerHTML = mensaje;
    elemntoh6.innerHTML = conusuario;
    elemto_span.innerHTML=tiempo;

    principal.setAttribute("id", conusuario);

    
    secundario.appendChild(elemntoh6);
    secundario.appendChild(elemento_p);
    //secundario.appendChild(sep);
    

    principal.appendChild(elemento_img);
    principal.appendChild(secundario);
    principal.appendChild(elemto_span);

    

    
    
    if(tipo=='unico'){
        //div1.insertBefore(td, theFirstChild);
        
        div1.insertBefore(principal, theFirstChild);
        div1.insertBefore(sep, theFirstChild);
    }else{
        div1.appendChild(principal);
        div1.appendChild(sep);
    }

    
    //div1.appendChild(sep);
    
    function saludo()
        {
        
        let h6_texto = document.getElementById("h6_texto");
        h6_texto.innerHTML = conusuario;
        h6_texto.innerHTML = conusuario;

        let imagenperfil = document.getElementById("cabecera_foto_perfil"); 
    
        imagenperfil.setAttribute("src",DIR_HOST + "/mensajes/media/"  +fotoperfil)
        imagenperfil.setAttribute("alt","")
        

        ultimaconexion(conusuario);
        
        //div3.innerHTML = conusuario;
        
        cargadato();
        
        
        };
    
    principal.addEventListener('click',saludo,true); 

}