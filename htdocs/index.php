<?php

function ParagraphWrap($string) {
	return "<p>" . $string . "</p>" . "\n";
}

$command = escapeshellcmd('C:\Users\tbodi\AppData\Local\Programs\Python\Python38-32\python.exe generate_plots.py');
$output = shell_exec($command);

echo $output;

$temp_plot = "<img src=p1.png>";
$hum_plot = "<img src=p2.png>";
$brtag ="<br>";

echo $temp_plot . $brtag . "\n";
echo $hum_plot


?>