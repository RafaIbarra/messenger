import {cargarmensaje} from './cargarchat.js'
import {DIR_HOST} from './variables.js'
export function cargadato(){
    
    let usuario = document.getElementById("h6_texto").innerText;
    const div4 = document.getElementById("Chat");
    let val=usuario.length;
    if (val >0){
       
    
        const urlchat = DIR_HOST +'/mensajes/chats/' + usuario;
        
        
        
        let cupcakes = Array.prototype.slice.call(document.getElementsByClassName("row no-gutters"), 0);
       
        let valor=cupcakes.length;
        
        if (valor >0){
            for(let i of cupcakes){
                i.remove();
            } 
    
        };

        
    
        fetch(urlchat)
        .then((resp) => resp.json())
        .then(function(data) {
        let authors = data;
    
        return authors.forEach((e) => { 
            
        
            if (e.chat.envio==usuario){
                
                cargarmensaje("row no-gutters","col-md-5","chat-bubble chat-bubble--left",e.chat.mensaje,e.chat.fechacorta);
            }
            else{
                
                cargarmensaje("row no-gutters","col-md-5 offset-md-7","chat-bubble chat-bubble--right",e.chat.mensaje,e.chat.fechacorta);
            }
            
            
    
        });
        
        })
    };

    
}
cargadato();

