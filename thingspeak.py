import urllib
import time
import httplib

DS18B20 = "/sys/bus/w1/devices/28-0416936589ff/w1_slave"

r = 0

while True:

	r += 1
	
	f = open(DS18B20, "r")
	data = f.read()
	data_split = data.split()
	t = float(data_split[21][2:])/1000

	params = urllib.urlencode({'field1': t, 'key': 'BRU4KLV7KB8KYROY'})
	headers = {"Content-typZZe" : "application/x-www-form-urlencoded","Accept": "text/plain"}
	conn = httplib.HTTPConnection("api.thingspeak.com:80")
	f.close()
	conn.request("POST", "/update", params, headers)
	try:
		response = conn.getresponse()
		
		print (t)
		print (response.status, response.reason)
		conn.close()
	except:
		print ("connection failed")
	time.sleep(1)



