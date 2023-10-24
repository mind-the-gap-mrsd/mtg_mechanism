import socket
import RPi.GPIO as GPIO
import time
def actuate(i, p):
    #try:
    if i == 0:
        print("extending")
        p.ChangeDutyCycle(5)  # extend
        print("extended")
        #time.sleep(10)
    elif i ==1:
        p.ChangeDutyCycle(10)  # retract\
        #time.sleep(10)

        #GPIO.cleanup()


if __name__=="__main__":
    LIMIT_SWITCH_PIN_1=27 #currently connected to ls for test
    LIMIT_SWITCH_PIN_2=22
    LIMIT_SWITCH_PIN_3=17 
    ACTUONIX = 18
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(LIMIT_SWITCH_PIN_1, GPIO.IN,  pull_up_down=GPIO.PUD_UP)
    GPIO.setup(LIMIT_SWITCH_PIN_2, GPIO.IN,  pull_up_down=GPIO.PUD_UP)
    GPIO.setup(LIMIT_SWITCH_PIN_3, GPIO.IN,  pull_up_down=GPIO.PUD_UP)
    GPIO.setup(ACTUONIX, GPIO.OUT)
    p = GPIO.PWM(ACTUONIX, 50)
    p.start(0)

    time.sleep(5)

    switch_state_khepera_1 = GPIO.input(LIMIT_SWITCH_PIN_1) #LIMIT_SWITCH_PIN_1)
    switch_state_khepera_2 = GPIO.input(LIMIT_SWITCH_PIN_2)
    switch_state_actuonix = GPIO.input(LIMIT_SWITCH_PIN_3)
    
    while True:
        try:
            #print(switch_state_khepera_1, switch_state_khepera_2)
            if GPIO.input(LIMIT_SWITCH_PIN_1) == True and GPIO.input(LIMIT_SWITCH_PIN_2) == True:
                
                actuate(0, p)
                #time.sleep(10)
                print(switch_state_actuonix)
                time.sleep(10)
                break
            #else:
                #actuate(1, p)
                #time.sleep(10)
        except KeyboardInterrupt:
            p.stop()
            GPIO.cleanup()
            break
            
