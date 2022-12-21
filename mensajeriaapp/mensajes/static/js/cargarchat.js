export function cargarmensaje(
    clasediv1,clasediv2,clasemensaje,textomensaje,textofecha
    )
    {
        let cantidad = Array.prototype.slice.call(document.getElementsByClassName("row no-gutters"), 0);
    
        let ide=cantidad.length

        const divprincipal = document.getElementById("Chat");
        let me = document.createElement("div");
        let divuno= document.createElement("div");
        let divdos= document.createElement("div");
        let fechamensaje=document.createElement("p");

        divuno.setAttribute("class",clasediv1);
        divdos.setAttribute("class",clasediv2);
        me.setAttribute("class",clasemensaje);
        me.setAttribute("id",ide);

        fechamensaje.innerHTML=textofecha;
        me.innerHTML=textomensaje;
        me.appendChild(fechamensaje);
        divdos.appendChild(me);
            
        divuno.appendChild(divdos);
        divprincipal.appendChild(divuno);
        document.getElementById(ide).scrollIntoView(true)
}
