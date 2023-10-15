import socket
#import RPi.GPIO as GPIO
import time
 
# Define the listening address and ports on the Raspberry Pi
listen_address = '0.0.0.0'  # Listen on all available network interfaces
flags_port = 12345
bool_flags_port = 12346
string_values_port = 12347

# Function to receive integer flags on the Raspberry Pi
def receive_integer_flags(listen_address, flags_port):
    print("Receiving flags")
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        #s.setblocking(False)
        s.bind((listen_address, flags_port))
        print("Bound")
        s.listen()
        print("Listened")
        conn, addr = s.accept()
        #print("Connected to: " + address[0] + ":" + str(address[1]))
        with conn:
            data = conn.recv(1024)
            
            return int(data.decode())
        

def receive_string_values(listen_address, string_values_por):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        #s.setblocking(False)
        s.bind((listen_address, string_values_port))
        s.listen()
        conn, addr = s.accept()
        #with conn:
        data = conn.recv(1024)
        s.close()
        return data.decode()
        



# GPIO.setmode(GPIO.BCM)
# GPIO.setup(18, GPIO.OUT) #use pinout to identify pins, 18 is 6th pin from top right
# p = GPIO.PWM(18, 50)

# p.start(5)

# while True:
# # Example usage on the Raspberry Pi
#         integer_flag = receive_integer_flags(listen_address, 12346)
#         print(f"Received Integer Flag: {integer_flag}")

# # print(f"Received Integer Flag: {integer_flag}")
# #print(f"Received Boolean Flag: {boolean_flag}")

# #print(f"Received String Values: {string_values}")

