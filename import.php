<?php
require_once('lib.php');

$data = new DataManager(new ConsoleLogger());
$data->importData();