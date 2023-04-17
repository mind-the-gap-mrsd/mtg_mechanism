import rospy
from std_msgs.msg import Int32MultiArray
import requests
from Adafruit_IO import Client

ADAFRUIT_IO_USERNAME = "ysudhansh"
ADAFRUIT_IO_KEY = "aio_FNkZ38Hy1iXvCb7n1Pk0nqxWRav9"
aio = Client(username=ADAFRUIT_IO_USERNAME, key=ADAFRUIT_IO_KEY)

def callback(msg):
    flags = msg.data
    aio.send("mtg-mechanism.k114", flags[0])
    aio.send("mtg-mechanism.k115", flags[1])
    aio.send("mtg-mechanism.k116", flags[2])
    print("Coupling commands sent")

    # ThingSpeak
    
    # req = "https://api.thingspeak.com/update.json?api_key=O6ZS7W3R8LZVC301" # &field1=0&field2=3&field3=1
    # for i in range(len(flags)):
    #     req += "&field" + str(i+1) + "=" + str(flags[i])
    # response = requests.get(req)
    # body = int.from_bytes(response.content, 'little', signed=True)
    # if (body == 48):
    #     print("Error")
    # else:
    #     print("Coupling commands sent")

if __name__ == "__main__":
    rospy.init_node("mtg_mechanism", anonymous=True)
    rospy.Subscriber("mtg_mechanism", Int32MultiArray, callback)
    rospy.spin()