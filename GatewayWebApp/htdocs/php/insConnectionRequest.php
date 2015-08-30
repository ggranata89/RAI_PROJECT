<?php


   include 'mysql_connect.php';



   $data = file_get_contents("php://input");

   $body = json_decode($data,true);



   $CodGateway=$body["CodGateway"];
   $ConnectionRequest=$body["ConnectionRequest"];



   $sql="INSERT INTO task (REGISTER,VALUE,COD_GATEWAY) VALUES ('ConnectionRequest', '$ConnectionRequest','$CodGateway');";

   mysqli_query($con,$sql);



   mysqli_close($con);





?>
