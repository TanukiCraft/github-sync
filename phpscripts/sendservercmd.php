<?php
require('MulticraftAPI.php');
$api = new MulticraftAPI('Redacted', 'Redacted', 'Redaced');
print_r($api->sendConsoleCommand($argv[1], $argv[2]));