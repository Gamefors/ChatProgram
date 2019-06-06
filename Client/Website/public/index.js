function sendData(data) {
  var xhttp = new XMLHttpRequest();
  
  xhttp.open('POST', 'http://localhost:7000');
  xhttp.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
  xhttp.send(data);
}

function register(){
    username = document.getElementById("username").value;
    password = document.getElementById("password").value;
    sendData(username + ":" + password)
  }