const express = require("express");
const bodyParser = require("body-parser");
const mysql = require("mysql");

const mysqlConfig = {//TODO: add config file where these thing are being read from .json
  host: "192.168.0.122",
  user: "chatprogram",
  password: "safepw",
  database: "chat"
};

const connection = mysql.createConnection(mysqlConfig);

const app = express();
app.set("view engine", "pug");
app.use("/public", express.static(__dirname + "/public"));
app.use(bodyParser.urlencoded({ extended: true }));
app.use(bodyParser.json());

app.get("/", (req, res) => {
    res.render("index");
  });

app.get("/register", (req, res) => {
    res.render("register");
});

app.get("/login", (req, res) => {
  res.render("login");
});

app.get("/adminPanel", (req, res) => {
  res.render("adminPanel");
});

app.post("/register",function(req,res){//FIXME:TODO: chech if account already exist etc. with username  to and send someting back so user know he registered right or wrong
  let data = req.body;
  data = JSON.stringify(data);
  data = data.split(":");
  let username = data[0];
  let password = data[1];
  let email = data[2];
  username = username.slice(2);
  password = password
  email = email.substring(0, email.length-1);
  let registerStatement = "INSERT INTO accounts (username, password, email) VALUES ('" + username + "', '" + password + "'," + "'" + email + "')";
  connection.query(registerStatement);
  console.log("New Account Registered");
});

app.post("/login",function(req,res){
  let data = req.body;
  data = JSON.stringify(data);
  data = data.split(":");
  let username = data[0];
  let password = data[1];
  username = username.slice(2);
  password = password.substring(0, password.length-1);
  console.log(username + " tried to log in.")
  let loginStatement = "SELECT * FROM accounts WHERE username = '" + username + "' AND password = '" + password + "'";
  connection.query(loginStatement, function(err, result, fields){
    if (err) throw err;
    let sResult = JSON.stringify(result)
    if (sResult.length > 2){
      res.status(200).json({"succesfull":"succesfull"})//TODO: make this work
      console.log(username + " succesfully logged in.")
    }else{
      console.log(username + " couldn't log in.")
    }
  });
});

const server = app.listen(7000, () => {
    console.log("Started express node.js server (version: 1.0.0) on ip: " + server.address().address + " port: " + server.address().port);
  });
