import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
GPIO.setup(27, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(22, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(17, GPIO.IN, pull_up_down=GPIO.PUD_UP)
try:
	while True:
		if GPIO.input(27) == True:
			print("closed 27")
			time.sleep(0.3)
		else:
			print("Open 27")
			time.sleep(0.3)
		if GPIO.input(22) == True:
			print("closed 21")
			time.sleep(0.3)
		else:
			print("Open 22")   
			time.sleep(0.3)
		if GPIO.input(17) == True:
			print("closed 17")
			time.sleep(0.3)
		else:
			print("Open 17")   
			time.sleep(0.3)
except KeyboardInterrupt:
	GPIO.cleanup()
