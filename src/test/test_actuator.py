import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
GPIO.setup(18, GPIO.OUT) #use pinout to identify pins, 18 is 6th pin from top right
p = GPIO.PWM(18, 50)

p.start(0)

def actuate(i):
    try:
        if i == 0:
            p.ChangeDutyCycle(5)  # extend
            time.sleep(3)
        elif i ==1:
            p.ChangeDutyCycle(10)  # extend\
            time.sleep(3)
    except KeyboardInterrupt:
        p.stop()
        GPIO.cleanup()
i = int(input())
actuate(1)  

