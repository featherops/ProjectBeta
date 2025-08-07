<?php
if (isset($_POST['software_key'])) {
	# $software_key = htmlspecialchars($_POST['software_key']);
	$software_key_encoded = $_POST['software_key'];
	
	// Set Following values Correctly
	$servername = "localhost";
	$username = "root";
	$password = "";
	$dbname = "nekros";
	
	// Create connection
	$conn = new mysqli($servername, $username, $password, $dbname);
	
	// Check connection
	if ($conn->connect_error) {
		die("Connection failed: " . $conn->connect_error);
	}  
	
	$sql = "SELECT decrypt_key FROM nekros_keys WHERE software_key=?";
	$stmt = $conn->prepare($sql);
	$stmt->bind_param("s", $software_key_encoded);
	$stmt->execute();
	$result = $stmt->get_result();
	if ($result->num_rows > 0) {
		while($row = $result->fetch_assoc()) {
			echo $row["decrypt_key"];
		}
	} else {
		echo "Failed";
	}
	$stmt->close();
	$conn->close();
}
else {
	echo "Failed";
}

# SQL Query : SELECT decrypt_key FROM ranspy_keys WHERE software_key='Machine_ID'

?>
