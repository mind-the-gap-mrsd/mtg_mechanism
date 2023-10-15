import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
GPIO.setup(21, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(20, GPIO.IN, pull_up_down=GPIO.PUD_UP)

while True:
	if GPIO.input(20) == True:
		print("closed 20")
		time.sleep(0.3)
	else:
		print("Open 20")
		time.sleep(0.3)
	if GPIO.input(21) == True:
		print("closed 21")
		time.sleep(0.3)
	else:
		print("Open 21")   
		time.sleep(0.3)

