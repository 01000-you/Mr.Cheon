import time
import RPi.GPIO as GPIO
import random

GPIO.setmode(GPIO.BOARD)
GPIO.setup(16, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(3, GPIO.OUT)
while True:

	time.sleep(random.randint(1,5))
	GPIO.output(3, GPIO.HIGH)
	start = time.time()
	GPIO.wait_for_edge(16, GPIO.RISING)
	GPIO.output(3, GPIO.LOW)
	end = time.time()

	print(round(end - start,3), "seconds")
	time.sleep(1)
