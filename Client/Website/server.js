const express = require('express');
const bodyParser = require('body-parser');
const mysql = require('mysql');
const app = express();

const connection = mysql.createConnection({
  host: "localhost",
  user: "chatprogram",
  password: "safepw",
  database: "chat"
});

app.set('view engine', 'pug');
app.use("/public", express.static(__dirname + "/public"));
app.use(bodyParser.urlencoded({ extended: true }));
app.use(bodyParser.json());

app.get('/', (req, res) => {
    res.render('index');
  });

app.post("/",function(req,res){
  let username, password;
  let data = req.body;
  data = JSON.stringify(data);
  data = data.split(":");
  username = data[0];
  password = data[1];
  username = username.slice(2);
  password = password.substring(0, password.length-1);
  connection.connect(function(err) {
    if (err) throw err;
    console.log("Succesfully connected to DB.");
    var sql = "INSERT INTO accounts (username, password) VALUES ('" + username + "', '" + password + "')";
    connection.query(sql, function (err, result) {
      if (err) throw err;
      console.log("Succesfully inserted Username: " + username + " and Password: " + password + " into DB.");
    });
  });
});

const server = app.listen(7000, () => {
    console.log(`Express running → PORT ${server.address().port}`);
  });

