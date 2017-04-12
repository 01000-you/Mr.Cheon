Mission 4,5
===========
###온도센서에서 온도를 측정한 후, Thingspeak차트를 생성하고 mysqrl에 데이터를 저장하기!


##<mission.js> 소스코드

<pre><code>
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

</code></pre>

##<therm_m4,5.py> 소스코드

<pre><code>
import urllib
import time
import http.client
from urllib.request import urlopen

DS18B20 = "/sys/bus/w1/devices/28-0416936589ff/w1_slave"

r = 0

while True:

	r += 1
	f = open(DS18B20, "r")
	data = f.read()
	data_split = data.split()
	t = float(data_split[21][2:])/1000

	params = urllib.parse.urlencode({'field1': t, 'key': 'BRU4KLV7KB8KYROY'})
	headers = {"Content-typZZe" : "application/x-www-form-urlencoded","Accept": "text/plain"}
	conn = http.client.HTTPConnection("api.thingspeak.com:80")
	f.close()
	conn.request("POST", "/update", params, headers)
	try:
		response = conn.getresponse()
		print ("saved to tingspeak")
		conn.close()

	except:
		print ("connection failed")

	print("temperature = ", t)
	content = urlopen("http://127.0.0.1:3000/mysql/?temp="+str(t))
	print ("file save")

	time.sleep(10)

</code></pre>
