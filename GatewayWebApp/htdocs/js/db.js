$(document).ready(function(){

var page=0;

/*if(sessionStorage.getItem("page")!=null){
	page=parseInt(sessionStorage.getItem("page"));
	$("#numpage").val(page+1);
}else{
	page=0;
	$("#numpage").val(page+1);
}*/
		

var num_row_page=10;
var num_page=0;
var num_total_row;



var query="SELECT * FROM (SELECT f.ID as IDB,f.TIMESTAMP AS TIMESTAMP,(a.IL&0x1F) AS CODE_SENSOR,ut.DESCRIPTION AS TYPE,f.ID_NODE,us.DESCRIPTION AS STATE,f.COD_RX_DEVICE,f.CL,f.BC,f.ST,att.DESCRIPTION AS APP_TYPE,f.RN,a.TP,a.TMR,a.NRT,a.DATA FROM frame f,app_frame a,uart_state us,uart_type ut,app_type att WHERE a.COD_FRAME=f.ID  and f.STATE=us.CODE and f.TY=att.CODE and f.TYPE=ut.CODE UNION ALL SELECT f.ID,f.TIMESTAMP AS TIMESTAMP,'NULL',ut.DESCRIPTION AS TYPE,f.ID_NODE,us.DESCRIPTION AS STATE,f.COD_RX_DEVICE,f.CL,f.BC,f.ST,'NULL',f.RN,'NULL','NULL','NULL','NULL' FROM frame f,uart_state us,uart_type ut,app_type att WHERE f.TYPE=170 and f.STATE=us.CODE and f.TY=att.CODE and f.TYPE=ut.CODE) a "
var query_view=query+"ORDER BY a.TIMESTAMP ASC,a.IDB ASC LIMIT "+parseInt(page)*num_row_page+","+num_row_page
var last_query=query;
//var query_view="SELECT * FROM (SELECT f.ID as IDB,f.TIMESTAMP AS TIMESTAMP,(a.IL&0x1F) AS CODE_SENSOR,ut.DESCRIPTION AS TYPE,f.ID_NODE,us.DESCRIPTION AS STATE,f.COD_RX_DEVICE,f.CL,f.BC,f.ST,att.DESCRIPTION AS APP_TYPE,f.RN,a.TP,a.TMR,a.NRT,a.DATA FROM frame f,app_frame a,uart_state us,uart_type ut,app_type att WHERE a.COD_FRAME=f.ID  and f.STATE=us.CODE and f.TY=att.CODE and f.TYPE=ut.CODE UNION ALL SELECT f.ID,f.TIMESTAMP AS TIMESTAMP,'NULL',ut.DESCRIPTION AS TYPE,f.ID_NODE,us.DESCRIPTION AS STATE,f.COD_RX_DEVICE,f.CL,f.BC,f.ST,'NULL',f.RN,'NULL','NULL','NULL','NULL' FROM frame f,uart_state us,uart_type ut,app_type att WHERE f.TYPE=170 and f.STATE=us.CODE and f.TY=att.CODE and f.TYPE=ut.CODE) a where a.TIMESTAMP LIKE"
											//+ "'" +"%"+ $("#timestamp").val() +"%" +"'" 
											//+ "and a.TYPE LIKE" +"'" + $("#type").val() +"%" +"'"
											//+ "and a.ID_NODE LIKE" +"'" + $("#id_node").val() +"%" +"'"
											//+ "and a.BC LIKE" +"'" + $("#bc").val() +"%" +"'"
											//+ "and a.APP_TYPE LIKE" +"'" + $("#app_type").val() +"%" +"'"
											//+ "and a.DATA LIKE" +"'" + $("#data").val() +"%" +"'"
											//+ "and a.TP LIKE" +"'" + $("#txp").val() +"%" +"'"
											//+ "and a.NRT LIKE" +"'" + $("#nrt").val() +"%" +"'"
											//+ "and a.COD_RX_DEVICE LIKE" +"'" + $("#cod_rx").val() +"%" +"'"
											//+ "and a.STATE LIKE" +"'" + $("#state").val() +"%" +"'"
							




    $("#btnser").on('click', function (event) {
       var svalue=$('#cmbitem option:selected').text() 
       var text=$("#txtsearch").val();

       if(svalue=="TIMESTAMP"){
       		if($('#chkcon').prop('checked') ){
       			last_query=query+"where a.TIMESTAMP LIKE "+"'" +"%"+ text +"%" +"' ";
  	   		}else{
  	   			last_query=query+"where a.TIMESTAMP="+"'"+text+"'";
  	   		}
       }else if(svalue=="TYPE"){
			if($('#chkcon').prop('checked') ){
  	   			last_query=query+"where a.TYPE LIKE "+"'" +"%"+ text +"%" +"' ";
  	   		}else{
  	   		    last_query=query+"where a.TYPE="+"'"+text+"'";
  	   		}
       }else if(svalue=="ID_NODE"){
			if($('#chkcon').prop('checked') ){
  	   			last_query=query+"where a.ID_NODE LIKE "+"'" +"%"+ text +"%" +"' ";
  	   		}else{
  	   			last_query=query+"where a.ID_NODE="+"'"+text+"'";
  	   		}
       }else if(svalue=="BC"){
			if($('#chkcon').prop('checked') ){
  	   			last_query=query+"where a.BC LIKE "+"'" +"%"+ text +"%" +"' ";
  	   		}else{
  	   			last_query=query+"where a.BC="+"'"+text+"'";
  	   		}
       }else if(svalue=="APP_TYPE"){
       		if($('#chkcon').prop('checked') ){
  	   			last_query=query+"where a.APP_TYPE LIKE "+"'" +"%"+ text +"%" +"' ";
  	   		}else{
  	   			last_query=query+"where a.APP_TYPE="+"'"+text+"'";
  	   		}
       }else if(svalue=="DATA"){
       		if($('#chkcon').prop('checked') ){
  	   			last_query=query+"where a.DATA LIKE "+"'" +"%"+ text +"%" +"' ";
  	   		}else{
  	   			last_query=query+"where a.DATA="+"'"+text+"'";
  	   		}
       }else if(svalue=="TXP"){
       		if($('#chkcon').prop('checked') ){
  	   			last_query=query+"where a.TP LIKE "+"'" +"%"+ text +"%" +"' ";
  	   		}else{
  	   			last_query=query+"where a.TP="+"'"+text+"'";
  	   		}
       }else if(svalue=="NRT"){
       		if($('#chkcon').prop('checked') ){
  	   			last_query=query+"where a.NRT LIKE "+"'" +"%"+ text +"%" +"' ";
  	   		}else{
  	   			last_query=query+"where a.NRT="+"'"+text+"'";
  	   		}
       }else if(svalue=="COD_RX"){
       		if($('#chkcon').prop('checked') ){
  	   			last_query=query+"where a.COD_RX_DEVICE LIKE "+"'" +"%"+ text +"%" +"' ";
  	   		}else{
  	   			last_query=query+"where a.COD_RX_DEVICE="+"'"+text+"'";
  	   		}
       }else if(svalue=="STATE"){
       		if($('#chkcon').prop('checked') ){
  	   			last_query=query+"where a.STATE LIKE "+"'" +"%"+ text +"%" +"' ";
  	   		}else{
  	   			last_query=query+"where a.STATE="+"'"+text+"'";
  	   		}
       }

       if(text==""){
       		last_query=query;
       }

  	   	query_view=last_query+"ORDER BY a.TIMESTAMP ASC,a.IDB ASC LIMIT "+parseInt(page)*num_row_page+","+num_row_page
        $("#tblreport").empty();
		a();
    });


	function a(){
    	var requestCount = $.ajax({
			url: "php/reportCount.php",
			type: "POST",			
			dataType: "html",
			data: {sql:last_query}
		});

		requestCount.done(function(json) {
     		obj = JSON.parse(json);
     		num_total_row=parseInt(obj.NUM_APP_FRAME);
	 		num_page=(parseInt(parseInt(num_total_row)/parseInt(num_row_page))+1);
	 		$("#pagereport").empty();
	 		$("#pagereport").append("page: "+(parseInt(page)+1)+"/"+num_page);
	 		b();
		});
	}

	function b(){

		var request = $.ajax({
			url: "php/report.php",
			type: "POST",			
			dataType: "html",
			data: {sql:query_view}
		});

		request.done(function(json) {
		obj = JSON.parse(json);
		$("#tblreport").append("<tr id='header'>");
			$("#header").append("<th>TIMESTAMP</th>");
			$("#header").append("<th>TYPE</th>");
			$("#header").append("<th>ID NODE</th>");
			$("#header").append("<th>BC</th>");
			$("#header").append("<th>APP FRAME TYPE</th>");
			$("#header").append("<th>DATA</th>");
			$("#header").append("<th>TXP</th>");
			$("#header").append("<th>NRT</th>");
			$("#header").append("<th>CODE_RX_DEVICE</th>");
			$("#header").append("<th>STATE</th>");
		$("#tblreport").append("</tr>");

		crc_error=0;
		crc_ok=0;

		for(i=0;i<obj.list.length;i++){
			$("#tblreport").append("<tr id=r"+i+">");
				$("#r"+i).append("<td id=rc"+i+"1>"+obj.list[i].TIMESTAMP+"</td>");
				$("#r"+i).append("<td id=rc"+i+"2>"+obj.list[i].TYPE+"</td>");
				$("#r"+i).append("<td id=rc"+i+"3>"+obj.list[i].ID_NODE+"</td>");
				$("#r"+i).append("<td id=rc"+i+"4>"+obj.list[i].BC+"</td>");
				$("#r"+i).append("<td id=rc"+i+"5>"+obj.list[i].APP_TYPE+"</td>");
				$("#r"+i).append("<td id=rc"+i+"6>"+obj.list[i].DATA+"</td>");
				$("#r"+i).append("<td id=rc"+i+"7>"+obj.list[i].TP+"</td>");
				$("#r"+i).append("<td id=rc"+i+"8>"+obj.list[i].NRT+"</td>");
				$("#r"+i).append("<td id=rc"+i+"9>"+obj.list[i].COD_RX_DEVICE+"</td>");
				$("#r"+i).append("<td id=rc"+i+"10>"+obj.list[i].STATE+"</td>");

			$("#tblreport").append("</tr>");
		}

		sessionStorage.setItem("json",json);

		last_query_row=obj.num_rows;

	});	
   }

   a();




	function pages(e){

		var p=e.which;

		if(p==13){

		 	if($("#numpage").val()<=num_page&&$("#numpage").val()!=0){
		 		page=$("#numpage").val()-1;
		 	}else{
		 		page=0;
		 		$("#numpage").val(0);
		 	}

			query_view=last_query+"ORDER BY a.TIMESTAMP ASC,a.IDB ASC LIMIT "+parseInt(page)*num_row_page+","+num_row_page
       		$("#tblreport").empty();
		 	a();

		}

	}


	$("#numpage").bind('keypress',pages);

});