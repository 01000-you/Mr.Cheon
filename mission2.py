import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BOARD)

GPIO.setup(16, GPIO.IN, pull_up_down = GPIO.PUD_UP)
GPIO.setup(18,  GPIO.OUT)

while True:

	data = GPIO.input(16)
	print(data)
	GPIO.output(18, data)
	time.sleep(1)

