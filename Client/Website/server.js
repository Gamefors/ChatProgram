const express = require("express");
const bodyParser = require("body-parser");
const mysql = require("mysql");

const connection = mysql.createConnection({
  host: "localhost",
  user: "chatprogram",
  password: "safepw",
  database: "chat"
});

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

app.post("/register",function(req,res){//FIXME:TODO: chech if account already exist etc. only with username now later with emial to and send someting back so user know he registered right or wrong
  let data = req.body;
  data = JSON.stringify(data);
  data = data.split(":");
  let username = data[0];
  let password = data[1];
  let email = data[2];
  username = username.slice(2);
  password = password
  email = email.substring(0, email.length-1);//TODO: does not get whole email string fix this

  connection.connect(function(err) {
    if (err) throw err;
      console.log("Succesfully connected to DB.");
      var sql = "INSERT INTO accounts (username, password, email) VALUES ('" + username + "', '" + password + "'," + "'" + email + "')";
      connection.query(sql, function (err, result) {
    if (err) throw err;
      console.log("Succesfully inserted Username: " + username + ", Password: " + password + " and E-Mail: "+ email + " into DB.");
    });
  });
});

app.post("/login",function(req,res){//FIXME: 1 check if acoount exits then check if pw right,for all send alert
  console.log("requested login not implemented");
  //TODO: make mysql request if pw is corect an dshi
});

const server = app.listen(7000, () => {
    console.log(`Express running → PORT ${server.address().port}`);
  });

