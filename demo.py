import os
import rospy
from geometry_msgs.msg import Twist
import signal
import time
import subprocess

cmd = "python3 mech.py"
proc = subprocess.Popen(cmd, shell=True)

# back to front: 116-114-115

amar = rospy.Publisher("mtg_agent_bringup_node/amar/cmd_vel", Twist, queue_size=1)
akbar = rospy.Publisher("mtg_agent_bringup_node/akbar/cmd_vel", Twist, queue_size=1)
anthony = rospy.Publisher("mtg_agent_bringup_node/anthony/cmd_vel", Twist, queue_size=1)

rospy.init_node("demo", anonymous=True)
rate = rospy.Rate(10)

state = 0
crossTime = 3
decoupleTime = 2

def coupleAndRam():
    print("ramming")
    os.system("rostopic pub -1 /mtg_mechanism std_msgs/Int32MultiArray 'data: [1,1,1]'")
    while True:
        amarMsg = Twist()
        akbarMsg = Twist()
        anthonyMsg = Twist()

        amarMsg.linear.x = -0.0
        akbarMsg.linear.x = -0.15
        anthonyMsg.linear.x = 0.2

        amar.publish(amarMsg)
        akbar.publish(akbarMsg)
        anthony.publish(anthonyMsg)
        rate.sleep()
    # while True:
    #     pass

def crossGap(now, t):
    print("crossing")
    while rospy.Time.now() < now + rospy.Duration.from_sec(t):
        amarMsg = Twist()
        akbarMsg = Twist()
        anthonyMsg = Twist()

        amarMsg.linear.x = 0.8
        akbarMsg.linear.x = 0.8
        anthonyMsg.linear.x = 0.8

        amar.publish(amarMsg)
        akbar.publish(akbarMsg)
        anthony.publish(anthonyMsg)
        print("crossing")
        rate.sleep()

def decoupleAndSeparate(now, t):
    print("decouple")
    os.system("rostopic pub -1 /mtg_mechanism std_msgs/Int32MultiArray 'data: [5,5,5]'")
    time.sleep(10)
    os.system("rostopic pub -1 /mtg_mechanism std_msgs/Int32MultiArray 'data: [0,0,0]'")
    time.sleep(3)
    while rospy.Time.now() < now + rospy.Duration.from_sec(t):
        amarMsg = Twist()
        akbarMsg = Twist()
        anthonyMsg = Twist()

        amarMsg.linear.x = -0.1
        akbarMsg.linear.x = 0.0
        anthonyMsg.linear.x = -0.2

        akbar.publish(akbarMsg)
        amar.publish(amarMsg)
        anthony.publish(anthonyMsg)
        print("decouple")
        rate.sleep()

def handler(sig, frame):
    crossGap(rospy.Time.now(), crossTime)
    decoupleAndSeparate(rospy.Time.now(), decoupleTime)
    proc.kill()
    exit(1)

def quitter(sig, frame):
    proc.kill()
    exit(1)

signal.signal(signal.SIGINT, handler)
signal.signal(signal.SIGTSTP, quitter)
coupleAndRam()