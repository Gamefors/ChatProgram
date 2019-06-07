function sendData(data, type) {
  var xhttp = new XMLHttpRequest();
  xhttp.open("POST", "http://localhost:7000/" + type);
  xhttp.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
  xhttp.send(data);
}

function register(){
    username = document.getElementById("username").value;
    password = document.getElementById("password").value;
    email = document.getElementById("email").value;
    sendData(username + ":" + password + ":" + email, "register");
    alert("FIXME: should return to login page DONT register again server will crash otherwise")
}

function login(){
  username = document.getElementById("username").value;
  password = document.getElementById("password").value;
  sendData(username + ":" + password, "login");
  alert("FIXME:TODO: should direct to other website dont login again other wise server will crash")
}


  