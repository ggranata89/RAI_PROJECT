<?php

   include 'mysql_connect.php';

   $data = file_get_contents("php://input");
   $body = json_decode($data,true);
   $code= $body['code'];
   $result = mysqli_query($con,"DELETE FROM task WHERE COD_GATEWAY = '$code'");

   mysqli_close($con);


?>