var express = require('express');
var app = express();
var fs = require('fs');
mysql = require('mysql');
var date = new Date();

var connection =  mysql.createConnection({
	host: 'localhost',
	user: 'sensor',
	password: 'mypassword',
	database: 'data'
})

connection.connect(function(err) {
	if(err){
		console.error(err);
	}
});

r= {};
r.seq = 0;
r.type = 'T';
r.device = '102';
r.unit = '0';
r.ip = "127.0.0.1";
r.value = 0;

app.get('/', function (req, res){
    var qstr = 'select * from sensors where time > date_sub(now(), INTERVAL 1 DAY) ' ;
        
	
	connection.query(qstr, function(err, rows, cols){
		if (err) {
			//throw err;
			res.send('query error: '+ qstr);
			return;
		}
		var html = "<!doctype html><html><body>";
		  html += "<H1> Sensor Data for Last 24 Hours</H1>";
		  html += "<table border=1 cellpadding=3 cellspacing=0>";
		  html += "<tr><td>Seq#<td>Time Stamp<td>Temperature";
		
		  for (var i=0; i<rows.length; i++) {
		  	html += "<tr><td>"+i+"<td>"+ JSON.stringify(rows[i].time)+"<td>"+ JSON.stringify((rows[i].value));
      
		 }
		  html += "</table>";
		  html += "</body></html>";
		  res.send(html);
		
	});
			
})


app.get("/mysql", function(req, res){
    var qstr = 'select * from sensors where time > date_sub(now(), INTERVAL 1 DAY) ' ;
        
	
	connection.query(qstr, function(err, rows, cols){
		if (err) {
			//throw err;
			res.send('query error: '+ qstr);
			return;
		}
	    r.value = req.query.temp;
	console.log("Get data\n" + JSON.stringify(req.query));

	fs.appendFile('LOG.TXT', JSON.stringify(req.query)+","+r.ip+","+date+ "\n", function (err){
		if(err) throw err;
	});
	
    connection.query('insert into sensors set ?',r, function(err, rows, cols){
		if(err){
		    throw err;
	
		}
		console.log("Insert data in Mysql");
	});
	res.send("Data Access " + rows.length + " records");
	});

});


app.listen(3000, function (){
	console.log('Example app listening on port 3000!');
});
