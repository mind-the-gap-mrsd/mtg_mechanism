
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
    try:
        if i == 0:
            print("extending")
            p.ChangeDutyCycle(5)  # extend
            print("extended")
            time.sleep(10)
        elif i ==1:
            p.ChangeDutyCycle(10)  # retract\
            time.sleep(10)
    except KeyboardInterrupt:
        p.stop()
        GPIO.cleanup()


def receiver():
    print("Started limit switch sequence")
    LIMIT_SWITCH_PIN_1=20 #currently connected to ls for test
    LIMIT_SWITCH_PIN_2=21
    ACTUONIX = 18
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(LIMIT_SWITCH_PIN_1, GPIO.IN,  pull_up_down=GPIO.PUD_UP)
    GPIO.setup(LIMIT_SWITCH_PIN_2, GPIO.IN,  pull_up_down=GPIO.PUD_UP)
    GPIO.setup(ACTUONIX, GPIO.OUT)
    p = GPIO.PWM(ACTUONIX, 50)
    p.start(0)
    
    time.sleep(5)
    #send_string_values("Couple\n", send_address, send_port)
    #couple_command = "Couple\n"
    #decouple_command = "Decouple\n"
   # while True:
    switch_state_khepera_1 = GPIO.input(21) #LIMIT_SWITCH_PIN_1)
    #switch_state_khepera_2 = GPIO.input(22) 
    switch_state_actuonix = GPIO.input(20) #LIMIT_SWITCH_PIN_2)

    while switch_state_actuonix == False:
        print("Not latched")
        #if switch_state_khepera_1 == True: #and switch_state_khepera_2 == True:
        #    actuate(0, p) #Extend actuonix
    
    return True

def fucker():
    ser = serial.Serial('/dev/serial0', baudrate=9600, timeout=1)
    #couple_command = receive_string_values(receive_address, fsm_port)
    #if couple_command:
    couple_command = "Decouple\n"
    print(couple_command)
    try:
        ser.write(couple_command.encode('utf-8'))
        ser.flush()
    except KeyboardInterrupt:
        print("stfuing")
        stop_command = "stfu\n"
        ser.write(stop_command.encode('utf-8'))
            #Extend Nima till second limit switch is hit
	
