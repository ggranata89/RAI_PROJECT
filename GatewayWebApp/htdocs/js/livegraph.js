	$(document).ready(function(){
			
	
		        setInterval(updateData,5000);

			var requestRxCode = $.ajax({
         			url: "php/getNodeRx.php",
         			type: "POST",     
         			dataType: "html",
         			data: {}
        		});

			requestRxCode.done(function(json){
			     obj = JSON.parse(json);
			     for(i=0;i<obj.cod_rx_device.length;i++){
 				val=obj.cod_rx_device[i].id;
                                $("#txtnoderxnum").append("<option>"+val+"</option>");
			     } 
			       $.ajax({
    							type: 'POST',
    							url: 'php/getNodeTx.php',
    							data:  JSON.stringify({"id":$('#txtnoderxnum option:selected').text()}),
    							success: function(json) {
      								obj = JSON.parse(json);
				        			$("#txtnodetxnum").empty();
   								for(i=0;i<obj.tx_code.length;i++){
 									val=obj.tx_code[i].id;
                                					$("#txtnodetxnum").append("<option>"+val+"</option>");
			     					}
  							}
    				});
			});


			$(function(){
				$("#txtnoderxnum").change(function() {
  					$.ajax({
    							type: 'POST',
    							url: 'php/getNodeTx.php',
    							data:  JSON.stringify({"id":$('#txtnoderxnum option:selected').text()}),
    							success: function(json) {
      								obj = JSON.parse(json);
				        			$("#txtnodetxnum").empty();
   								for(i=0;i<obj.tx_code.length;i++){
 									val=obj.tx_code[i].id;
                                					$("#txtnodetxnum").append("<option>"+val+"</option>");
			     					}
  							}
    					});
				});
			});

			

			$(function(){
    					$("#txtnodetxnum").change(function() {
  						$.ajax({
    							type: 'POST',
    							url: 'php/getSensorCode.php',
    							data:  JSON.stringify({"id":$('#txtnodetxnum option:selected').text()}),
    							success: function(json) {
      								obj = JSON.parse(json);
				        			$("#txtnodesensornum").empty();
   								for(i=0;i<obj.sensor_code.length;i++){
					  				val=obj.sensor_code[i].id;
                                	  				$("#txtnodesensornum").append("<option value="+val+">"+(parseInt(val)&0x1F)+"</option>");
								}
  							}
    						});
				
					});
			});
	

        		var request = $.ajax({
         			url: "php/report.php",
         			type: "POST",     
         			dataType: "html",
         			data: {sql:"SELECT * FROM (SELECT f.TIMESTAMP AS TIMESTAMP,ut.DESCRIPTION AS TYPE,f.ID_NODE,us.DESCRIPTION AS STATE,f.COD_RX_DEVICE,f.CL,f.BC,f.ST,att.DESCRIPTION AS APP_TYPE,f.RN,(a.IL&0x1F) AS CODE_SENSOR,a.TP,a.TMR,a.NRT,a.DATA FROM frame f,app_frame a,uart_state us,uart_type ut,app_type att WHERE a.COD_FRAME=f.ID and f.STATE=us.CODE and f.TY=att.CODE and f.TYPE=ut.CODE) a where a.ID_NODE LIKE" 
                      + "'" +"%"+ $('#txtnodetxnum option:selected').text() +"%" +"'" 
                      + "and a.COD_RX_DEVICE LIKE" +"'" + $('#txtnoderxnum option:selected').text() +"%" +"'"
                       + "and a.CODE_SENSOR LIKE" +"'" + $('#txtnodesensornum option:selected').text() +"%" +"'"
			
                    		}
        		});
			

      			request.done(function(json){
          		var line1 = [];
          		obj = JSON.parse(json);
          		

			for(i=0;i<obj.list.length;i++){
                		line1.push(parseInt(obj.list[i].DATA));		
          		}

		
  
         		var plot1 = $.jqplot('chart1', [line1], {
            			title: '', 
              			seriesDefaults: { 
                		showMarker:false,
                		pointLabels: { show:true } 
              		}
         	});

     	});



		function updateData(){


			var request = $.ajax({
				url: "php/report.php",
				type: "POST",			
				dataType: "html",
				data: {sql:"SELECT * FROM (SELECT f.TIMESTAMP AS TIMESTAMP,ut.DESCRIPTION AS TYPE,f.ID_NODE,us.DESCRIPTION AS STATE,f.COD_RX_DEVICE,f.CL,f.BC,f.ST,att.DESCRIPTION AS APP_TYPE,f.RN,(a.IL&0x1F) AS CODE_SENSOR,a.TP,a.TMR,a.NRT,a.DATA FROM frame f,app_frame a,uart_state us,uart_type ut,app_type att WHERE a.COD_FRAME=f.ID and f.STATE=us.CODE and f.TY=att.CODE and f.TYPE=ut.CODE) a where a.ID_NODE LIKE" 
											+ "'" +"%"+ $('#txtnodetxnum option:selected').text() +"%" +"'" 
											+ "and a.COD_RX_DEVICE LIKE" +"'" + $('#txtnoderxnum option:selected').text()+"%" +"'"
                       + "and a.CODE_SENSOR LIKE" +"'" + $('#txtnodesensornum option:selected').text() +"%" +"'"
										}
			 });

			 request.done(function(json) {
    	     
          var line1 = [];

          obj = JSON.parse(json);
          for(i=0;i<obj.list.length;i++){
                line1.push(parseInt(obj.list[i].DATA));
          }


          var plot1 = $.jqplot('chart1', [line1], {
            title: '', 
              seriesDefaults: { 
                showMarker:false,
                pointLabels: { show:true } 
              }
          }).replot();	

  		  });
     }


    });
