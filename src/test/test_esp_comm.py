import serial
import time
# Configure the serial port
ser = serial.Serial('/dev/serial0', baudrate=9600, timeout=1)

def get_input():
    i = input()
    if i == "couple":
        data_to_send = "couple\n"
    else:
        data_to_send = "decouple\n"
    return data_to_send

data_to_send = get_input()
try:
    ser.write(data_to_send.encode('utf-8'))
    print("aaaa")
except Exception as e:
    print("Failed because", e)
    time.sleep(5)



