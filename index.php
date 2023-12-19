<!DOCTYPE html>
<html lang="pl">

<head>
  <meta charset="UTF-8">
  <meta http-equiv="X-UA-Compatible" content="IE=edge">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Lewitująca piłka</title>
  <link rel="stylesheet" href="style.css">
</head>

<body>
  <div class="navbar">
    <form method="post" name="parametry">
      <div class="dropdown">
        <button class="dropbtn">Regulator &#x25BE;</button>
        <div class="dropdown-content">
          <a href="#">PID</a>
          <a href="#">Fuzzy Logic</a>
        </div>
      </div>
      <input type="hidden" id="regulator" name="regulator" value="">
      <input type="number" id="pozycja" name="pozycja" step="0.1" placeholder="Pozycja zadana" data-placement="bottom"
        title="Pozycja zadana">
      <input type="number" id="kp" name="kp" step="0.1" placeholder="Wzmocnienie" data-placement="bottom"
        title="Wzmocnienie">
      <input type="number" id="ti" name="ti" step="0.1" placeholder="Czas zdwojenia" data-placement="bottom"
        title="Czas zdwojenia">
      <input type="number" id="td" name="td" step="0.1" placeholder="Czas wyprzedzenia" data-placement="bottom"
        title="Czas wyprzedzenia">
      <button type="submit" class="button" name="button1" id="submitForm">&#x25B6;</button>
    </form>
  </div>

  <span id="output" style="font-weight: bold; color:red"></span>

  <div id="tester" style="width: 1200px; height: 500px;"></div>
  <div class="info-bar">
    <span id="regulatorInfo"></span>
  </div>

  <script src="https://cdn.plot.ly/plotly-2.20.0.min.js" charset="utf-8"></script>
  <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.5.1/jquery.min.js"></script>
  <script src="app.js"></script>
</body>

</html>


<?php
header("Cache-Control: no-cache, no-store, must-revalidate");
header("Cache-Control: post-check=0, pre-check=0", false);
header("Pragma: no-cache");
header("Expires: 0");

if ($_SERVER['REQUEST_METHOD'] == 'POST') {
  button1();
}

function button1()
{
  $regulator = $_POST['regulator'];
  $pozycja = $_POST['pozycja'];
  $kp = $_POST['kp'];
  $ti = $_POST['ti'];
  $td = $_POST['td'];
  if (empty($regulator)) {
    $regulator = 'PID';
  }
  if (empty($pozycja)) {
    $pozycja = 45;
  }
  if (empty($kp)) {
    $kp = 0.1;
  }
  if (empty($ti)) {
    $ti = 10;
  }
  if (empty($td)) {
    $td = 2;
  }

  if ($regulator == 'PID') {
    $command = escapeshellcmd('python pid.py ' . $pozycja . ' ' . $kp . ' ' . $ti . ' ' . $td);
  } else {
    $command = escapeshellcmd('python fuzzy.py ' . $pozycja);
  }
  shell_exec($command);
  exit; // Kończy działanie skryptu PHP po zakończeniu skryptu Python
}
?>