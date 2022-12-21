    import {carganoversacion} from './cc.js'
    import {cargarmensaje} from './cargarchat.js'
    import {cargar_conectados} from './conectados.js'
    import {DIR_HOST_W} from './variables.js'
    
    const remitente = document.getElementById('remitente').innerText;
    const logeado = document.getElementById('remitente').innerText;
    let destino = new String;
    let banderacontrol=new String;
    banderacontrol='no';

    function enviarlinea(s){    
        
        chatSocket.send(JSON.stringify({
          'message': '',
          'remitente': remitente,
          'destinatario': '',
          'fechahora':'En Linea',
          'logeado':'',
          'accion':'conexion',
          
        }))
      
      
    }
    function enviarultimaconexion(s){
      
      const dt = new Date();
      const padL = (nr, len = 2, chr = `0`) => `${nr}`.padStart(2, chr);
      let fechaconexion=`${
                  
        padL(dt.getDate())}/${
        padL(dt.getMonth()+1)}/${
        dt.getFullYear().toString().slice(-2)} ${
        padL(dt.getHours())}:${
        padL(dt.getMinutes())}`;
          
          
        chatSocket.send(JSON.stringify({
          'message': '',
          'remitente': remitente,
          'destinatario': '',
          'fechahora':fechaconexion,
          'logeado':'',
          'accion':'conexion',
          
        }))
        
    }

      document.addEventListener("visibilitychange", event => { 
        if (document.visibilityState == "visible") { 
            
            enviarlinea();
            banderacontrol='si';
          } 
            
        else { 
              
              enviarultimaconexion();
              banderacontrol='si';
              } 
        })


  

      document.onclick=function(e){
        const id = e.target.getAttribute("id");
        if(id !== 'submit'){
          
            enviarlinea();
        }
        
        
        

          
      };
      
      document.querySelector('#submit').onclick = function (e) {
            destino = document.getElementById('h6_texto').innerText;
            
            const dt = new Date();
            const padL = (nr, len = 2, chr = `0`) => `${nr}`.padStart(2, chr);

            let fechahora=`${
                    
                    padL(dt.getDate())}/${
                    padL(dt.getMonth()+1)}/${
                    dt.getFullYear().toString().slice(-2)} ${
                    padL(dt.getHours())}:${
                    padL(dt.getMinutes())}`;
                    //:${padL(dt.getSeconds())}`;


            
            const messageInputDom = document.querySelector('#chat-text');
            const message = messageInputDom.value;
            const accion="enviomensaje";
            const conexion="conexion"
            if(message.length >0 ){
              chatSocket.send(JSON.stringify({
                'message': message,
                'remitente': remitente,
                'destinatario': destino,
                'fechahora':fechahora,
                'logeado':logeado,
                'accion':accion,
                
    
                }));
                
                
                messageInputDom.value = '';
                let cant = document.getElementById("cantidadtexto");
                cant.innerHTML='0/200' ;
            } else{
              // window.alert('El mensaje no puede estar en blanco');
              swal("Atencion!", "No puede enviar un mensaje en blanco!", "error");
            }
            
            
            
      };  

    const roomName = 'usuario';

    const chatSocket = new WebSocket(
        'ws://' +
         //window.location.host + 
         DIR_HOST_W+
        '/ws/mensajes/' +
        roomName +
        '/'+ logeado +'/'
      );

    chatSocket.onopen = function(e) {
      console.log("[open] Conexión establecida");
      
      };
      let consersacionselecionada=document.getElementById('h6_texto').innerText;
      
    
    chatSocket.onmessage = function (e) {
      
      
      const data = JSON.parse(e.data);
      
      if (data.accion=='enviomensaje'){
          const cabecera_destino=document.getElementById('h6_texto').innerText;
          if (data.remitente==remitente){
      
            carganoversacion(data.destinatario,data.message,data.fechahora);
            cargarmensaje("row no-gutters","col-md-5 offset-md-7","chat-bubble chat-bubble--right",data.message,data.fechahora);
            
          } else {

            if (remitente==data.destinatario && cabecera_destino==data.remitente ){

              if (remitente==data.destinatario){

                  cargarmensaje("row no-gutters","col-md-5","chat-bubble chat-bubble--left",data.message,data.fechahora);
                  

              }else{
                cargarmensaje("row no-gutters","col-md-5 offset-md-7","chat-bubble chat-bubble--right",data.message,data.fechahora);
                
              }
              carganoversacion(data.remitente,data.message,data.fechahora);
          
            }
            
          }
          if (data.destinatario==remitente){
            carganoversacion(data.remitente,data.message,data.fechahora);
            
          }
      } else{
            
            let destino_llega = document.getElementById('h6_texto').innerText;
            if (destino_llega == data.remitente){
              var divhora = document.getElementById('id_conexion');
              divhora.innerHTML=data.fechahora;
                        
              };
            if(remitente!==data.remitente){
                cargar_conectados(data.remitente,data.fechahora);
            };
      };
      



    };   
    