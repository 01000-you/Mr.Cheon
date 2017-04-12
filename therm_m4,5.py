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

