
import RPi.GPIO as GPIO
import time
import serial
from client import send_integer_flags, send_string_values
from server import receive_integer_flags, receive_string_values
address = '192.168.151'

receive_address =  '0.0.0.0'
receive_port = 12345
#Actuonix actuator
def actuate(i, p):
    if i == 0:
        print("extending")
        p.ChangeDutyCycle(5)  # extend
        print("extended")

    elif i ==1:
        p.ChangeDutyCycle(10)  # retract\


def receiver():
    print("Started limit switch sequence")
    LIMIT_SWITCH_PIN_1=22 #currently connected to ls for test
    LIMIT_SWITCH_PIN_2=27
    LIMIT_SWITCH_PIN_ACTUONIX = 17
    ACTUONIX = 18
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(LIMIT_SWITCH_PIN_1, GPIO.IN,  pull_up_down=GPIO.PUD_UP)
    GPIO.setup(LIMIT_SWITCH_PIN_2, GPIO.IN,  pull_up_down=GPIO.PUD_UP)
    GPIO.setup(LIMIT_SWITCH_PIN_ACTUONIX, GPIO.IN,  pull_up_down=GPIO.PUD_UP)
    GPIO.setup(ACTUONIX, GPIO.OUT)
    p = GPIO.PWM(ACTUONIX, 50)
    p.start(0)
    
    time.sleep(5)
    if GPIO.input(LIMIT_SWITCH_PIN_1) == True and GPIO.input(LIMIT_SWITCH_PIN_2) == True:
                
        actuate(0, p)
        print(GPIO.input(LIMIT_SWITCH_PIN_ACTUONIX))

def couple():
    ser = serial.Serial('/dev/serial0', baudrate=9600, timeout=1)

    data_to_send = "couple\n"


    try:
        ser.write(data_to_send.encode('utf-8'))
        print("aaaa")
    except Exception as e:
        print("Failed because", e)
        time.sleep(5)
            #Extend Nima till second limit switch is hit
	
