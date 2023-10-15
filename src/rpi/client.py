import socket
import time
# Define the Raspberry Pi's IP address and ports
raspberry_pi_address = '192.168.2.181'  # Replace with the Raspberry Pi's IP
flags_port = 12345
bool_flags_port = 12346
string_values_port = 12347

# Function to send integer flags from the Ubuntu machine to the Raspberry Pi
def send_integer_flags(value, address, flags_port): 
    print("Sending flag")
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        print("Connecting")
        s.connect((address, flags_port))

        print("Connected")
        try:
            s.sendall(str(value).encode())
        except Exception as e:
            print(e)
        print("Sent")

# Function to send boolean flags from the Ubuntu machine to the Raspberry Pi
# def send_boolean_flags(value):
#     with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
#         s.connect((raspberry_pi_address, bool_flags_port))
#         s.sendall(str(value).encode())

# # Function to send comma-delimited string of values from the Ubuntu machine to the Raspberry Pi
def send_string_values(values, address, string_values_port):
    print("Sending string values")
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        #while True:
        #try:
        #s.setblocking(False)
        s.connect((address, string_values_port))
        s.sendall(values.encode())
        print("Sent string values")
            #break
        #except BlockingIOError:
        #    time.sleep(1)
        s.close()

# # Example usage on the Ubuntu machine
# central_compute_address = '192.168.2.151'
# listen_port = 12346

# while True:
#     send_integer_flags(0, central_compute_address, listen_port)
#     print("Sent")
# # send_boolean_flags(True)
# # send_string_values("1,2,3,4,5")
