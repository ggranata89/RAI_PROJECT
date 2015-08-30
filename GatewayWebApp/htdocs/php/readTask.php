<?php


   include 'mysql_connect.php';

   $data = file_get_contents("php://input");
   $body = json_decode($data,true);
   $code= $body['code'];
   $result = mysqli_query($con,"SELECT * FROM task WHERE COD_GATEWAY = '$code' ");
   $num=mysqli_num_rows($result);
   
   $json='{"task"'.':[';
   while($row = mysqli_fetch_array($result)) { 
   		$num=$num-1;
   		$json.="{";
   		$json.='"register-name":'.'"'.$row['REGISTER'].'",';
   		$json.='"value":'.'"'.$row['VALUE'].'",';
   		$json.='"cod_gateway":'.'"'.$row['COD_GATEWAY'].'"';
   		if($num==0)
   		 $json.="}";
   		else
   		 $json.="},";
   }
   $json.="]}";
   echo $json;

   mysqli_close($con);


?>