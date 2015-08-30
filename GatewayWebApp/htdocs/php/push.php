<?php

   include 'mysql_connect.php';

   $data = file_get_contents("php://input");
   $body = json_decode($data,true);

   $count =count($body["frame"]);
 
 	for($i=0;$i<$count;$i++){
    	 $sql="";
  

     	$type=$body["frame"][$i]["TYPE"];
     	$id_node=$body["frame"][$i]["ID_NODE"];
     	$state=$body["frame"][$i]["STATE"];
	 	$cod_rx_device=$body["frame"][$i]["COD_RX_DEVICE"]; 

     	$cl=$body["frame"][$i]["CL"];
     	$bc=$body["frame"][$i]["BC"];
     	$st=$body["frame"][$i]["ST"];

     	$ty=$body["frame"][$i]["TY"];
     	$rn=$body["frame"][$i]["RN"];
	

		$insert=1;
		mysqli_query($con,"START TRANSACTION");
			$sql="INSERT INTO frame (TYPE,ID_NODE,STATE,COD_RX_DEVICE,CL,BC,ST,TY,RN) VALUES ('$type', '$id_node', '$state','$cod_rx_device','$cl','$bc','$st','$ty','$rn');";
    		$tmp = mysqli_query($con,$sql);
    		$insert=($insert&$tmp);
    		$tmp=mysqli_query($con,"SET @frame_id  = LAST_INSERT_ID()");
    		$insert=($insert&$tmp);
    		$sub_count = count($body["frame"][$i]["payload"]);
   			for($j=0;$j<$sub_count;$j++){
      			$il=$body["frame"][$i]["payload"][$j]["IL"];
      			$tp=$body["frame"][$i]["payload"][$j]["TP"];
      			$tmr=$body["frame"][$i]["payload"][$j]["TMR"];
      			$nrt=$body["frame"][$i]["payload"][$j]["NRT"];
      			$data=$body["frame"][$i]["payload"][$j]["DATA"];
      			$sql="INSERT INTO app_frame (IL,TP,TMR,NRT,DATA,COD_FRAME) VALUES ('$il','$tp','$tmr','$nrt','$data',@frame_id);";
      			$tmp = mysqli_query($con,$sql);
      			$insert=($insert&$tmp);
   			}

			if($insert) {
    			mysqli_query($con,"COMMIT");
			echo "ok";
			} else {
    			mysqli_query($con,"ROLLBACK");
			echo "error";
			}
		}

mysqli_close($con);

?>
