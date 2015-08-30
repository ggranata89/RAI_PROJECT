<?php

	include 'mysql_connect.php';


	if(isset($_POST['sql']))
	  $sql=$_POST['sql'];
	




    
	$result = mysqli_query($con,$sql);
    $num=mysqli_num_rows($result); 

    $cnum=$num;

	
	echo '{';
	echo '"list":';
	echo '[';

		while($row = mysqli_fetch_array($result)) {

			$num=$num-1;
			echo '{';
				echo '"TIMESTAMP":'.'"'.$row['TIMESTAMP'].'",';
				echo '"TYPE":'.'"'.$row['TYPE'].'",';
				echo '"ID_NODE":'.'"'.$row['ID_NODE'].'",';
				echo '"CL":'.'"'.$row['CL'].'",';
				echo '"IL":'.'"'.$row['CODE_SENSOR'].'",';
				echo '"BC":'.'"'.$row['BC'].'",';
				echo '"ST":'.'"'.$row['ST'].'",';
				echo '"RN":'.'"'.$row['RN'].'",';
				echo '"APP_TYPE":'.'"'.$row['APP_TYPE'].'",';
				echo '"DATA":'.'"'.$row['DATA'].'",';
  				echo '"TP":'.'"'.$row['TP'].'",';
  				echo '"NRT":'.'"'.$row['NRT'].'",';
  				echo '"COD_RX_DEVICE":'.'"'.$row['COD_RX_DEVICE'].'",';
  				echo '"STATE":'.'"'.$row['STATE'].'"';
  			if($num==0)
  				echo '}';
  	    	else
  	    		echo '},';  
  		}	
	
	echo '],';
	echo '"num_rows":'.'"'.$cnum.'"';
	echo '}';

	mysqli_close($con);
	
?>