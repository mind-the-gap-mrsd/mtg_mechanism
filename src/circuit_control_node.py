import socket
import time
import rospy
from std_msgs.msg import Int16
# Define the Raspberry Pi's IP address and ports
'''
Agent 1 wants to couple with Agent 2
Computer listens for feedback from agent 2 on pi_to_computer port
Computer sends a command to agent 1 when feedback is received on computer_to_pi_port
'''

        
if __name__ == '__main__':

    agent_1 = '192.168.2.123' #This agent will extend Nema
    agent_2 = '192.168.2.181' #This agent will send limit switch feedback
    listen_address = '0.0.0.0'
    computer_to_pi_port = 12345
    pi_to_computer_port = 12346
    #Establish server (listener)
    s_from_agent_2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
    s_from_agent_2.setblocking(False)
    s_from_agent_2.bind((listen_address, pi_to_computer_port))
    print("Started listening at port", pi_to_computer_port)

    s_to_agent_1 = None
    #s_to_nema_pi = None

    while True:
        s_from_agent_2.listen(5)
        print("Listening")
        
        try: #Will send data to agent 1 only if data is received from agent 2
            print("accepting")
            conn, addr = s_from_agent_2.accept()
            #print("Connected to: " + address[0] + ":" + str(address[1]))
            print("Printing data received")
            #with conn:
            data = conn.recv(1024)
                #if data:
            print(int(data.decode()))
            if s_to_agent_1 is None:
                s_to_agent_1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s_to_agent_1.connect((agent_1, computer_to_pi_port)) 
                print("Connected to pi/port", agent_1, computer_to_pi_port)
            else:
                s_to_agent_1 = s_to_agent_1
            s_to_agent_1.sendall(str(1).encode())
            print ("Sent command", 1)
            
        except Exception as e: #if you don't get feedback, can't do anything
            print("Waiting for circuit feedback")
        


