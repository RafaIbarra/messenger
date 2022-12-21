
import {ultimaconexion} from './datosconexciones.js'
import {cargadato} from './chats.js'
import {DIR_HOST} from './variables.js'

const myModal = document.getElementById('myModal')
const myInput = document.getElementById('myInput')
const divmodal = document.getElementById("datosmodal");
var datos=[];
document.querySelector('#mostrarmodal').onclick = function (e) {
    divmodal.replaceChildren()
    const urlmodal = DIR_HOST+'/mensajes/listadousuarios/';
    fetch(urlmodal)
    .then((resp) => resp.json())
    .then(function(data) {
        
        datos = data;
        
        return datos.forEach((e) => {    
        

        let contenedor_usuario="lista_contenedor" + e.disponibles.user_name
        let contenedor_lista= document.createElement("div");
        contenedor_lista.setAttribute("class","contenedoractivo");
        contenedor_lista.setAttribute("id", contenedor_usuario);
        contenedor_lista.setAttribute("data-bs-dismiss", "modal");
    


        let usuario_lista="usuario_lista" + e.disponibles.user_name
        let principal_usuario = document.createElement("div");
        principal_usuario.setAttribute("class","friend-drawer friend-drawer--onhover")
        principal_usuario.setAttribute("id", usuario_lista);

        let elemento_img_lista=document.createElement("img");
        elemento_img_lista.setAttribute("class","profile-image-conectados")
        elemento_img_lista.setAttribute("src",DIR_HOST+"/mensajes/media/"  +e.disponibles.image)
        elemento_img_lista.setAttribute("alt","")

        let secundario_lista = document.createElement("div");
        secundario_lista.setAttribute("class","text")

        let elemntoh6_lista=document.createElement("h6");
        elemntoh6_lista.innerHTML = e.disponibles.user_name;

        secundario_lista.appendChild(elemntoh6_lista);
        principal_usuario.appendChild(elemento_img_lista);
        principal_usuario.appendChild(secundario_lista);
        

        
        contenedor_lista.appendChild(principal_usuario);
        divmodal.appendChild(contenedor_lista);
        
        
        function saludo()
        {
        
            let h6_texto = document.getElementById("h6_texto");
            h6_texto.innerHTML = e.disponibles.user_name;
            h6_texto.innerHTML = e.disponibles.user_name;

            let imagenperfil = document.getElementById("cabecera_foto_perfil"); 
            imagenperfil.setAttribute("src",DIR_HOST+"/mensajes/media/"  +e.disponibles.image)
            imagenperfil.setAttribute("alt","")
            
            ultimaconexion(e.disponibles.user_name);
            
            cargadato();
            
            
        };
    
        contenedor_lista.addEventListener('click',saludo,true); 


    
    });
    
    })

}


document.querySelector('#buscarusuario').oninput  = function (e) {
    
    let palabras = document.getElementById("buscarusuario").value;

    divmodal.replaceChildren()
    const filtrar=()=>{
        
        for(let nombre of datos){
            
            let buscar=nombre.disponibles.user_name;
            
            if(buscar.indexOf(palabras) !== -1){
                
                let contenedor_usuario="lista_contenedor" + nombre.disponibles.user_name
                let contenedor_lista= document.createElement("div");
                contenedor_lista.setAttribute("class","contenedoractivo");
                contenedor_lista.setAttribute("id", contenedor_usuario);
                contenedor_lista.setAttribute("data-bs-dismiss", "modal");
        
        
                let usuario_lista="usuario_lista" + nombre.disponibles.user_name
                let principal_usuario = document.createElement("div");
                principal_usuario.setAttribute("class","friend-drawer friend-drawer--onhover")
                principal_usuario.setAttribute("id", usuario_lista);
        
                let elemento_img_lista=document.createElement("img");
                elemento_img_lista.setAttribute("class","profile-image-conectados")
                elemento_img_lista.setAttribute("src",DIR_HOST+"/mensajes/media/"  +nombre.disponibles.image)
                elemento_img_lista.setAttribute("alt","")
        
                let secundario_lista = document.createElement("div");
                secundario_lista.setAttribute("class","text")
        
                let elemntoh6_lista=document.createElement("h6");
                elemntoh6_lista.innerHTML = nombre.disponibles.user_name;
        
                secundario_lista.appendChild(elemntoh6_lista);
                principal_usuario.appendChild(elemento_img_lista);
                principal_usuario.appendChild(secundario_lista);
                
        
                
                contenedor_lista.appendChild(principal_usuario);


                function saludo()
                {
                
                    let h6_texto = document.getElementById("h6_texto");
                    h6_texto.innerHTML = nombre.disponibles.user_name;
                    h6_texto.innerHTML = nombre.disponibles.user_name;

                    let imagenperfil = document.getElementById("cabecera_foto_perfil"); 
                    imagenperfil.setAttribute("src",DIR_HOST+"/mensajes/media/"  +nombre.disponibles.image)
                    imagenperfil.setAttribute("alt","")
            

                    ultimaconexion(nombre.disponibles.user_name);
                    
                    cargadato();
                    
                    
                };
            
                contenedor_lista.addEventListener('click',saludo,true); 

                divmodal.appendChild(contenedor_lista);
            
            }
        }
    }
    filtrar();
    
    
  }


myModal.addEventListener('shown.bs.modal', () => {

myInput.focus()


})