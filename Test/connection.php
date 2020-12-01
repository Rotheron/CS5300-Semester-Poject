<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN">
<html>
<body>
<?php

$hostname = "cs-class-db.srv.mst.edu";
$username = "lff8gw";
$password = "BigGamer7!!";
$db = "lff8gw";

$dbconnect=mysqli_connect($hostname,$username,$password,$db);

if ($dbconnect->connect_error) {
  die("Database connection failed: " . $dbconnect->connect_error);
}

?>

<table border="1" align="center">
<tr>
  <td>ALBUMS</td>
</tr>

<?php

$query = mysqli_query($dbconnect, "SELECT * FROM ALBUMS")
   or die (mysqli_error($dbconnect));

while ($row = mysqli_fetch_array($query)) {
  echo
   "<tr>
    <td>{$row[1]}</td>
   </tr>\n";
 }

?>
</table>
</body>
</html>