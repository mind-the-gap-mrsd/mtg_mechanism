import socket
import time
import rospy
from std_msgs.msg import Int16
# Define the Raspberry Pi's IP address and ports
'''
Simple node to receive coupling commands as a message and publish them to the raspberry pi via sockets
Values for coupling are published to a topic, read and republished
0 - extend, 1 - retract 
Assumes server is running on raspberry pi.
'''

# Function to send integer flags from the Ubuntu machine to the Raspberry Pi
def send_integer_flags(value): 
    print("Sending flag")
    raspberry_pi_address = '192.168.2.181'  # Replace with the Raspberry Pi's IP
    flags_port = 12345

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        print("Connecting")
        s.connect((raspberry_pi_address, flags_port))

        print("Connected")
        try:
            s.sendall(str(value).encode())
        except Exception as e:
            print(e)
        print("Sent")


def callback(data):
    send_integer_flags(data.value)
    

if __name__ == '__main__':
    rospy.init_node('coupling_actuator', anonymous=True)

    rospy.Subscriber("actuate_topic", Int16, callback) #pls rename 

    rospy.spin()  