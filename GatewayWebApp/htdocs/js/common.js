$( document ).ready(function(){
 
    $("#btnhome").on('click', function (event) {
   		var link=document.createElement("a");
		link.href="/index.html";
		document.body.appendChild(link);
		link.click();
		document.body.removeChild(link);    
    });

     $("#btn_exit").on('click', function (event) {
     	alert("ciao");
   		window.close();   
    });

  
});