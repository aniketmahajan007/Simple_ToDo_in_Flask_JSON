let add = ()=>{
   let task = document.getElementById("todo_write").value;
   fetch('https://flasktodo-aniket.herokuapp.com/add',{
      method: 'POST',
      headers: {
      'Accept': 'application/json',
      'Content-Type': 'application/json'
    },
      body: JSON.stringify({task: task })
   }).then((response) =>{
      (response.json()).then((data)=>{

         if(data["Success"] !== undefined ){
            location.reload();
         }else{
            alert("Error Occurred")
         }
      });
   }).catch(()=>{
      alert("Network error occurred")
   })
}
document.getElementById("add_in_list").addEventListener('click',add)
document.getElementById("todo_write").addEventListener('keydown',(e)=>{
   if(e.key === "Enter"){add();}
});
Array.from(document.getElementsByClassName("remove_task")).forEach((element) => {
   element.addEventListener('click',()=>{
      const id = element.getAttribute("id").match(/\d+/)[0];
      if(confirm("Do you want to remove this tasks")){
         fetch('https://flasktodo-aniket.herokuapp.com/remove/'+id,{
               method: 'DELETE',
               headers: {
               'Accept': 'application/json',
               'Content-Type': 'application/json'
             }
         }).then((response) =>{
               (response.json()).then((data)=>{
                  
                  if(data["Success"] !== undefined ){
                     const li = element.closest('li');
                     li.parentNode.removeChild(li);
                  }else{
                     alert("Error Occurred")
                  }
               });
         }).catch(()=>{
               alert("Network error occurred")
         })
      }
   })
});
Array.from(document.getElementsByClassName("items_checkbox")).forEach((element)=>{
      element.addEventListener(`click`, ()=>{
         const id = element.getAttribute("id").match(/\d+/)[0];
         if(!element.checked){
            if(confirm("Do you want to uncheck this Task")){
               fetch('https://flasktodo-aniket.herokuapp.com/unchecked/'+id,{
                  method: 'PUT',
                  headers: {
                  'Accept': 'application/json',
                  'Content-Type': 'application/json'
                }
               }).then((response) =>{
                  (response.json()).then((data)=>{
                     
                     if(data["Success"] !== undefined ){
                        element.closest('li').classList.remove("completed")
                     }else{
                        alert("Error Occurred")
                     }
                  });
               }).catch(()=>{
                  alert("Network error occurred")
               })
            }
         }else{
            if(confirm("Do you want to checklist this Task")){
               fetch('https://flasktodo-aniket.herokuapp.com/checked/'+id,{
                  method: 'PUT',
                  headers: {
                  'Accept': 'application/json',
                  'Content-Type': 'application/json'
                }
               }).then((response) =>{
                  (response.json()).then((data)=>{
                     
                     if(data["Success"] !== undefined ){
                        element.closest('li').classList.add("completed")
                     }else{
                        alert("Error Occurred")
                     }
                  });
               }).catch(()=>{
                  alert("Network error occurred")
               })
            }
         }
      });
});
document.getElementById("clear_all_task").addEventListener('click',()=>{
   if(confirm('Are you sure you want to remove all task?')){
      fetch('https://flasktodo-aniket.herokuapp.com/clear',{
                  method: 'DELETE',
                  headers: {
                  'Accept': 'application/json',
                  'Content-Type': 'application/json'
                }
               }).then((response) =>{
                  (response.json()).then((data)=>{
                     if(data["Success"] !== undefined ){
                       document.getElementById("all_tasked").innerHTML="";
                       const clear_all_task = document.getElementById("clear_all_task")
                       clear_all_task.parentNode.removeChild(clear_all_task)
                     }else{
                        alert("Error Occurred")
                     }
                  });
               }).catch(()=>{
                  alert("Network error occurred")
               })
   }
});