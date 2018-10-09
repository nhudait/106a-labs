#!/usr/bin/env python
#The line above tells Linux that this file is a Python script,
#and that the OS should use the Python interpreter in /usr/bin/env
#to run it. Don't forget to use "chmod +x [filename]" to make
#this script executable.

#Import the dependencies as described in example_pub.py
import tf2_ros 
import sys
import rospy
from geometry_msgs.msg import TransformStamped

#Define the method which contains the node's main functionality
def listener(source_frame, target_frame):
    tfBuffer = tf2_ros.Buffer()
    tfListener = tf2_ros.TransformListener(tfBuffer)
    rate = rospy.Rate(10)

    # Loop until the node is killed with Ctrl-C
    while not rospy.is_shutdown():
        try:
            trans = tfBuffer.lookup_transform(target_frame, source_frame, rospy.Time())
            print(trans)
        except (tf2_ros.LookupException, tf2_ros.ConnectivityException, tf2_ros.ExtrapolationException):
            continue

        rate.sleep()

#Python's syntax for a main() method
if __name__ == '__main__':
    rospy.init_node('tf2_echo_listener')
    listener(sys.argv[2], sys.argv[1])