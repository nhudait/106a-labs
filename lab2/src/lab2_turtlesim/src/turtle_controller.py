#!/usr/bin/env python
import rospy
import sys
from geometry_msgs.msg import Twist

tName = sys.argv[1]
topic = tName + '/cmd_vel'

def talker():
    #Create an instance of the rospy.Publisher object which we can 
    #use to publish messages to a topic. This publisher publishes 
    #messages of type std_msgs/String to the topic /chatter_talk
    pub = rospy.Publisher(topic, Twist, queue_size=10)

    # Loop until the node is killed with Ctrl-C
    while not rospy.is_shutdown():
        text = raw_input("Enter a command and press <Enter>: ")
        pub_twist = Twist()

        if text == "w":
            pub_twist.linear.x = 2.0
        elif text == "a":
            pub_twist.angular.z = 2.0
        elif text == "s":
            pub_twist.linear.x = -2.0
        elif text == "d":
            pub_twist.angular.z = -2.0

        # Publish our string to the 'chatter_talk' topic
        pub.publish(pub_twist)
      
# This is Python's sytax for a main() method, which is run by default
# when exectued in the shell
if __name__ == '__main__':
    # Check if the node has received a signal to shut down
    # If not, run the talker method
    try:
        rospy.init_node('talker', anonymous=True)
        talker()
    except rospy.ROSInterruptException: pass