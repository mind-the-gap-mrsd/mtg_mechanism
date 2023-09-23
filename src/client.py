import socket
import time
# Define the Raspberry Pi's IP address and ports
raspberry_pi_address = '192.168.2.181'  # Replace with the Raspberry Pi's IP
flags_port = 12345
bool_flags_port = 12346
string_values_port = 12347

# Function to send integer flags from the Ubuntu machine to the Raspberry Pi
def send_integer_flags(value): 
    print("Sending flag")
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        print("Connecting")
        s.connect((raspberry_pi_address, flags_port))

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
# def send_string_values(values):
#     with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
#         s.connect((raspberry_pi_address, string_values_port))
#         s.sendall(values.encode())

# Example usage on the Ubuntu machine
while True:
    send_integer_flags(0)
    print("Extending")
    time.sleep(100)
    send_integer_flags(1)
    print("Retracting")
    time.sleep(10)
# send_boolean_flags(True)
# send_string_values("1,2,3,4,5")
