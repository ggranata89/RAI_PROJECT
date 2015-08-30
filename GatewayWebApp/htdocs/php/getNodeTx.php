<?php


   include 'mysql_connect.php';

   $data = file_get_contents("php://input");
   $body = json_decode($data,true);
   $id= $body['id'];
   $result = mysqli_query($con,"SELECT DISTINCT ID_NODE FROM frame f WHERE f.COD_RX_DEVICE='$id'");
   $num=mysqli_num_rows($result);
   
   $json='{"tx_code"'.':[';
   while($row = mysqli_fetch_array($result)) { 
   		$num=$num-1;
   		$json.="{";
   		$json.='"id":'.'"'.$row['ID_NODE'].'"';
   		if($num==0)
   		 $json.="}";
   		else
   		 $json.="},";
   }
   $json.="]}";
   echo $json;

   mysqli_close($con);


?>
