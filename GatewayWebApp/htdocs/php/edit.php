<?php

   include 'mysql_connect.php';

   $data = file_get_contents("php://input");
   $body = json_decode($data,true);


   $CodGateway=$body["CodGateway"];

   $PeriodicTx=$body["PeriodicTx"];
   $ListenPort=$body["ListenPort"];

   if($PeriodicTx!=""){
   	$sql="INSERT INTO task (REGISTER,VALUE,COD_GATEWAY) VALUES ('PeriodicTx', '$PeriodicTx','$CodGateway');";
   	mysqli_query($con,$sql);
   }

   if($ListenPort!=""){
   	$sql="INSERT INTO task (REGISTER,VALUE,COD_GATEWAY) VALUES ('ListenPort', '$ListenPort','$CodGateway');";
   	mysqli_query($con,$sql);
   }

   mysqli_close($con);


?>
