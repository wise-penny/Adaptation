<?php

function getaliases($con) {
    $results = $con->query('SELECT username FROM ad_revs, chat WHERE (aim = "' . $_COOKIE['myemail'] . '" || start = "' .  $_COOKIE['myemail'] . '") && (aim = username || start = username) && username != "' .  $_COOKIE['myemail'] . '" ORDER BY last DESC');
    
    $c = [];
    $d = [];
    if ($results->num_rows > 0) {
        while ($row = $results->fetch_assoc()) {
            $c[] = $row['username'];
        }
    }
    
    $f = [];
    foreach ($c as $v)
        $f[] = $v;
        
    //echo json_encode($c);
    echo $c;
    setcookie("aliases", json_encode($f));
}

function getfilename($con) {
    $results = $con->query('SELECT filename FROM chat WHERE (aim = "' . $_COOKIE['myemail'] . '" && start = "' .  $_COOKIE['chataddr'] . '") || (aim = "' . $_COOKIE['chataddr'] . '" && start = "' .  $_COOKIE['myemail'] . '")');
    
    $d = "oajc";
    
    if ($results->num_rows == 1) {
        $row = $results->fetch_assoc();
        $d = $row['filename'];
    }
    setcookie("chatfile", $d);
}

$conn = mysqli_connect("localhost", "r0ot3d", "RTYfGhVbN!3$", "adrs", "3306") or die("Error: Cannot create connection");


if ($_GET['c'] == 1)
    getaliases($conn);
else if ($_GET['c'] == 2)
    getfilename($conn);
?>