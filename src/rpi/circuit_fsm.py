import socket
from circuit_functions import fucker, receiver
from server import receive_integer_flags
from client import send_string_values, send_integer_flags
import time
        
if __name__=="__main__":
    listen_address =  '0.0.0.0' #Listen on all IPs on the specified port
    computer_address = '192.168.2.151' #
    computer_to_pi_port = 12345
    pi_to_computer_port = 12346
    #Establish server (listener) first
    s_from_computer = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
    s_from_computer.setblocking(False)
    s_from_computer.bind((listen_address, computer_to_pi_port))
    print("Started listening at port", computer_to_pi_port)
    
    s_to_computer = None

    while True:

        #Listen on server
        s_from_computer.listen(5)
        try: #If data received, activate nema
            conn, addr = s_from_computer.accept()
            print("Received flag from computer")
            data = conn.recv(1024)
            fucker()
        except Exception as e: #Send data to the server when ready to couple
            ready_to_couple = receiver()
            if ready_to_couple: 
                if s_to_computer is None:
                    s_to_computer = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    s_to_computer.connect((computer_address, pi_to_computer_port))
                else:
                    s_to_computer = s_to_computer
    
                s_to_computer.sendall(str(1).encode())
            #pass
            print("Retrying connection")
            time.sleep(1)
