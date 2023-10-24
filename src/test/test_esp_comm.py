import serial
import time
# Configure the serial port
ser = serial.Serial('/dev/serial0', baudrate=9600, timeout=1)
#ser.open()
#try:
    #while True:
        # Send data to ESP8266
data_to_send = "couple\n"
#data_to_send +='\n'

try:
    ser.write(data_to_send.encode('utf-8'))
    print("aaaa")
except Exception as e:
    print("Failed because", e)


    # Read data from ESP8266
    #received_data = ser.readline().decode('utf-8')
    # print("Received from ESP8266:", received_data, end='')
    #ser.flush()
    time.sleep(5)

# except KeyboardInterrupt:
    
#     data_to_send = "stfu\n"
#     ser.write(data_to_send.encode('utf-8'))
#     print("stfuing")
#     ser.close()
# finally:
#     ser.write(data_to_send.encode('utf-8'))
#     print("stfuing")
#     ser.close()

