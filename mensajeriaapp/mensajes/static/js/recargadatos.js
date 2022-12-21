import {DIR_HOST} from './variables.js'
window.addEventListener("load",function(){
    makerequest();
});
async function makerequest(){
  let result=await fetch(DIR_HOST +'/mensajes/mismensajes/');
  
}

