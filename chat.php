<?php

function updateChatFile($con) {
    $filename = $_GET['b'];
    $sql = 'UPDATE `chat` SET `chat`.`altered` = `chat`.`last`, `chat`.`checked` = 0, last = CURRENT_TIMESTAMP WHERE filename = "' . $filename . '"';
    $results = $con->query($sql);
}

//$conn = mysqli_connect("localhost", "r0ot3d", "RTYfGhVbN!3$", "adrs", "3306") or die("Error: Cannot create connection");

$conn = mysqli_connect("localhost", "root", "", "adrs", "3306") or die("Error: Cannot create connection");

    $sql = 'SELECT alias FROM ad_revs WHERE username = "' . $_COOKIE['chatlabel'] . '"';
    $results = mysqli_query($conn,$sql);
    
    if ($results->num_rows > 0) {
        $row = $results->fetch_assoc();
        setcookie("facename", $row['alias']);
    }

    if (!isset($_SESSION))
        session_start();
    $v = "";
    $v = $_GET['a'];
    
    $filename = $_COOKIE['chatfile'];

    if (!file_exists('xml/' . $filename)) {
        file_put_contents('xml/' . $filename, "<?xml version='1.0'?><?xml-stylesheet type='text/xsl' href='chatxml.xsl' ?><messages></messages>");
        chmod('xml/' . $filename, 0644);
    }

    //$dom = new \DomDocument();
    $dom = simplexml_load_file("xml/" . $filename);

    $x = $dom->msg;
    $n = "";

    $tmpy = $dom->addChild("msg");
    $tmpy->addAttribute("alias", $_COOKIE['facename']);
    $tmp = $tmpy->addChild("text",$v);
    $tmp->addAttribute("time", time());
    $tmp->addAttribute("user", $_COOKIE['myemail']);
    $tmp->addAttribute("alias", $_COOKIE['myalias']);
    $dom->asXML('xml/' . $filename);

    updateChatFile($conn);

?>