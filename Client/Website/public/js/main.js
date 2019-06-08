function sendData(data, type) {
  var xhttp = new XMLHttpRequest();
  xhttp.open("POST", "http://localhost:7000/" + type);
  xhttp.setRequestHeader("Content-Type", "application/x-www-form-urlencoded");
  xhttp.send(data);
}

function register(){
  username = document.getElementById("username").value;
  password = document.getElementById("password").value;
  email = document.getElementById("email").value;
  sendData(username + ":" + password + ":" + email, "register");
  window.location.pathname = "/login";
  alert("Registering...");//TODO: add callback from node js server if succeded or not and display with alert
  return false;
}

function login(){
  username = document.getElementById("username").value;
  password = document.getElementById("password").value;
  sendData(username + ":" + password, "login");
  window.location.pathname = "/adminPanel";
  alert("Logging in...");//TODO: add callback from node js server if succeded or not and display with alert
  return false;
}