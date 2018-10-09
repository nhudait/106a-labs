#!/usr/bin/env python
import rospy
from my_chatter.msg import TimestampString

def talker():
    rospy.init_node('talker', anonymous=True)

    #Create an instance of the rospy.Publisher object which we can 
    #use to publish messages to a topic. This publisher publishes 
    #messages of type std_msgs/String to the topic /chatter_talk
    pub = rospy.Publisher('user_messages', TimestampString, queue_size=10)

    # Loop until the node is killed with Ctrl-C
    while not rospy.is_shutdown():
        text = raw_input("Please enter a line of text and press <Enter>: ")
        pub_ts = TimestampString()
        pub_ts.input = text
        pub_ts.time = rospy.get_time()

        # Publish our string to the 'chatter_talk' topic
        pub.publish(pub_ts)
      
# This is Python's sytax for a main() method, which is run by default
# when exectued in the shell
if __name__ == '__main__':
    # Check if the node has received a signal to shut down
    # If not, run the talker method
    try:
        talker()
    except rospy.ROSInterruptException: pass