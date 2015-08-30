<?php


   include 'mysql_connect.php';

   $data = file_get_contents("php://input");
   $body = json_decode($data,true);
   $id= $body['id'];
   $result = mysqli_query($con,"SELECT DISTINCT a.IL FROM app_frame a,frame f WHERE a.COD_FRAME=f.ID and f.ID_NODE= '$id' ");
   $num=mysqli_num_rows($result);
   
   $json='{"sensor_code"'.':[';
   while($row = mysqli_fetch_array($result)) { 
   		$num=$num-1;
   		$json.="{";
   		$json.='"id":'.'"'.$row['IL'].'"';
   		if($num==0)
   		 $json.="}";
   		else
   		 $json.="},";
   }
   $json.="]}";
   echo $json;

   mysqli_close($con);


?>
