const express = require('express');
const bodyParser = require('body-parser');
const app = express();


app.set('view engine', 'pug');
app.use("/public", express.static(__dirname + "/public"));
app.use(bodyParser.urlencoded({ extended: true }));
app.use(bodyParser.json())
app.get('/', (req, res) => {
    res.render('index');
  });

app.post("/",function(req,res){
  var data=req.body;
  console.log(data.split(":"))
});

const server = app.listen(7000, () => {
    console.log(`Express running → PORT ${server.address().port}`);
  });
