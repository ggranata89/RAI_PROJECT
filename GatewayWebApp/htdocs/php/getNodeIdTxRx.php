<?php

	include 'mysql_connect.php';


	$sql="SELECT DISTINCT COD_RX_DEVICE AS COD FROM frame"; 
    
	$result = mysqli_query($con,$sql);
	$num=mysqli_num_rows($result); 

	echo '{';
	echo '"cod_rx_device":';
    echo '[';
	
	while($row = mysqli_fetch_array($result)) {
		$num=$num-1;
		echo '{';
       		echo '"id":'.'"'.$row['COD'].'"';


       	if($num==0)
  			echo '}';
  	    else
  	    	echo '},'; 
  	}
  	echo "],";

	$sql="SELECT DISTINCT ID_NODE  FROM frame"; 
    $result = mysqli_query($con,$sql);
	$num=mysqli_num_rows($result); 

	echo '"id_node":';
    echo '[';
    while($row = mysqli_fetch_array($result)) {
		$num=$num-1;
		echo '{';
       		echo '"id":'.'"'.$row['ID_NODE'].'"';


       	if($num==0)
  			echo '}';
  	    else
  	    	echo '},'; 
  	}
  	echo "]";
echo '}';
  	mysqli_close($con);

	
	
	
?>
