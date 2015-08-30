$( document ).ready(function(){

    $("#btn_livegraph").on('click', function (event) {
    	var link=document.createElement("a");
		link.href="/livegraph.html";
		document.body.appendChild(link);
		link.click();
		document.body.removeChild(link);       
    });

    $("#btn_list").on('click', function (event) {
    	var link=document.createElement("a");
		link.href="/list.html";
		document.body.appendChild(link);
		link.click();
		document.body.removeChild(link);       
    });

    $("#btn_setting").on('click', function (event) {
    	var link=document.createElement("a");
		link.href="/edit.html";
		document.body.appendChild(link);
		link.click();
		document.body.removeChild(link);       
    });

    $("#btn_db").on('click', function (event) {
    	var link=document.createElement("a");
		link.href="/db.html";
		document.body.appendChild(link);
		link.click();
		document.body.removeChild(link);       
    });

});