import serial

# Configure the serial port
ser = serial.Serial('/dev/serial0', baudrate=9600, timeout=1)
#ser.open()
try:
    while True:
        # Send data to ESP8266
        data_to_send = str(input())
        data_to_send += '\n'
        print("aaaa")
        ser.write(data_to_send.encode('utf-8'))

        # Read data from ESP8266
        #received_data = ser.readline().decode('utf-8')
       # print("Received from ESP8266:", received_data, end='')
        ser.flush()

except KeyboardInterrupt:
    print("stfuing")
    data_to_send = "stfu\n"
    ser.write(data_to_send.encode('utf-8'))
    ser.close()

