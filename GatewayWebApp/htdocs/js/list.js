
$( document ).ready(function(){

	var last_query_row=0;
	var crc_ok=0;
	var crc_error=0;
	var y_scroll_position=0;

	var query_view="SELECT * FROM (SELECT * FROM(SELECT f.ID as IDB,f.TIMESTAMP AS TIMESTAMP,(a.IL&0x1F) AS CODE_SENSOR,ut.DESCRIPTION AS TYPE,f.ID_NODE,us.DESCRIPTION AS STATE,f.COD_RX_DEVICE,f.CL,f.BC,f.ST,att.DESCRIPTION AS APP_TYPE,f.RN,a.TP,a.TMR,a.NRT,a.DATA FROM frame f,app_frame a,uart_state us,uart_type ut,app_type att WHERE a.COD_FRAME=f.ID  and f.STATE=us.CODE and f.TY=att.CODE and f.TYPE=ut.CODE UNION ALL SELECT f.ID,f.TIMESTAMP AS TIMESTAMP,'NULL',ut.DESCRIPTION AS TYPE,f.ID_NODE,us.DESCRIPTION AS STATE,f.COD_RX_DEVICE,f.CL,f.BC,f.ST,'NULL',f.RN,'NULL','NULL','NULL','NULL' FROM frame f,uart_state us,uart_type ut,app_type att WHERE f.TYPE=170 and f.STATE=us.CODE and f.TY=att.CODE and f.TYPE=ut.CODE) a ORDER BY a.TIMESTAMP DESC,a.IDB DESC LIMIT 0,100) b ORDER BY b.TIMESTAMP ASC,b.IDB ASC";

	function exportTableToCSV($table, filename) {

        var $rows = $table.find('tr:has(td)'),

            // Temporary delimiter characters unlikely to be typed by keyboard
            // This is to avoid accidentally splitting the actual contents
            tmpColDelim = String.fromCharCode(11), // vertical tab character
            tmpRowDelim = String.fromCharCode(0), // null character

            // actual delimiter characters for CSV format
            colDelim = '";"',
            rowDelim = '"\r\n"',

            // Grab text from table into CSV formatted string
            csv = '"' + $rows.map(function (i, row) {
            		if(i>0){
                		var $row = $(row),
                    	$cols = $row.find('td');

                		return $cols.map(function (j, col) {
                    		var $col = $(col),
                        	text = $col.text();
                    		return text.replace('"', '""'); // escape double quotes
						}).get().join(tmpColDelim);
                	}
            }).get().join(tmpRowDelim)
                	.split(tmpRowDelim).join(rowDelim)
                	.split(tmpColDelim).join(colDelim) + '"',

            // Data URI
            csvData = 'data:application/csv;charset=utf-8,' + encodeURIComponent(csv);

		var downloadLink=document.createElement("a");
		downloadLink.href=csvData;
		var date=new Date;
		downloadLink.download=date.getDay()+"-"+date.getMonth()+"-"+date.getFullYear()+"  "+date.getHours()+" "+date.getMinutes()+" "+date.getSeconds();

		document.body.appendChild(downloadLink);
		downloadLink.click();
		document.body.removeChild(downloadLink);

    }

    $("#btnexport").on('click', function (event) {
        exportTableToCSV.apply(this, [$('#tblreport'), 'export.csv']);
    });



    $("#btnpie").on('click', function (event) {
    	var link=document.createElement("a");
		link.href="/dashboard.html";
		document.body.appendChild(link);
		link.click();
		document.body.removeChild(link);       
    });


    var request = $.ajax({
			url: "php/report.php",
			type: "POST",			
			dataType: "html",
			//data: {sql:"SELECT * FROM report" }
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

	request.fail(function(jqXHR, textStatus) {
		alert( "Request failed: " + textStatus );
	});



	function press(e){

		var p=e.which;

		if(p==13){
		 	updateTable();
		}
	}


	function updateTable(){
     		
     		var request = $.ajax({
				url: "php/report.php",
				type: "POST",			
				dataType: "html",
				data: {sql:query_view}
			});
		
			request.done(function(json) {
				obj = JSON.parse(json);

				crc_error=0;
				crc_ok=0;

				for(i=0;i<obj.list.length;i++){
				 	if(i<last_query_row&&i<obj.num_rows){
						$("#rc"+i+"1").html(obj.list[i].TIMESTAMP);
						$("#rc"+i+"2").html(obj.list[i].TYPE);
						$("#rc"+i+"3").html(obj.list[i].ID_NODE);
						$("#rc"+i+"4").html(obj.list[i].BC);
						$("#rc"+i+"5").html(obj.list[i].APP_TYPE);
						$("#rc"+i+"6").html(obj.list[i].DATA);
						$("#rc"+i+"7").html(obj.list[i].TXP);
						$("#rc"+i+"8").html(obj.list[i].NRT);
						$("#rc"+i+"9").html(obj.list[i].COD_RX);
						$("#rc"+i+"10").html(obj.list[i].STATE);

						if($("#chkscroll").is(':checked'))
							y_scroll_position=y_scroll_position+50;
						else
							y_scroll_position=0;

				 	}else if(i>=last_query_row&&i<obj.num_rows){
				 		$("#tblreport").append("<tr id=r"+i+">");
						$("#r"+i).append("<td id=rc"+i+"1>"+obj.list[i].TIMESTAMP+"</td>");
						$("#r"+i).append("<td id=rc"+i+"2>"+obj.list[i].TYPE+"</td>");
						$("#r"+i).append("<td id=rc"+i+"3>"+obj.list[i].ID_NODE+"</td>");
						$("#r"+i).append("<td id=rc"+i+"4>"+obj.list[i].BC+"</td>");
						$("#r"+i).append("<td id=rc"+i+"5>"+obj.list[i].APP_TYPE+"</td>");
						$("#r"+i).append("<td id=rc"+i+"6>"+obj.list[i].DATA+"</td>");
						$("#r"+i).append("<td id=rc"+i+"6>"+obj.list[i].TP+"</td>");
						$("#r"+i).append("<td id=rc"+i+"7>"+obj.list[i].NRT+"</td>");
						$("#r"+i).append("<td id=rc"+i+"8>"+obj.list[i].COD_RX_DEVICE+"</td>");
						$("#r"+i).append("<td id=rc"+i+"9>"+obj.list[i].STATE+"</td>");
						$("#tblreport").append("</tr>");

						if($("#chkscroll").is(':checked'))
							y_scroll_position=y_scroll_position+50;
					}

					if($("#chkscroll").is(':checked')){
						window.scrollTo(0,y_scroll_position);
					}
									
				}

				sessionStorage.setItem("json",json);

				for(i=obj.num_rows;i<last_query_row;i++){
					$("#r"+i).remove();
				}

				last_query_row=obj.num_rows;
			});	
	}

	setInterval(updateTable,1000);

	$("#timestamp").bind('keypress',press);
	$("#type").bind('keypress',press);
	$("#id_node").bind('keypress',press);
	$("#bc").bind('keypress',press);
	$("#app_type").bind('keypress',press);
	$("#txp").bind('keypress',press);
	$("#nrt").bind('keypress',press);
	$("#cod_rx").bind('keypress',press);
	$("#state").bind('keypress',press);
	$("#data").bind('keypress',press);


});