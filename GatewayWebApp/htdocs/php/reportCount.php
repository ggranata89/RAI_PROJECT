<?php

	include 'mysql_connect.php';

	if(isset($_POST['sql']))
	  $sql=$_POST['sql'];

    $sql= "SELECT COUNT(*) AS COUNT FROM (".$sql.")"." c";

    //$sql="SELECT COUNT(ID) AS COUNT FROM app_frame";    
	$result = mysqli_query($con,$sql);


		while($row = mysqli_fetch_array($result)) {
			echo '{';
				echo '"NUM_APP_FRAME":'.'"'.$row['COUNT'].'"';
  			echo '}';
  	   
  		}	
	

	mysqli_close($con);
	
?>