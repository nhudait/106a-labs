#!/usr/bin/env python
import rospy
from moveit_msgs.srv import GetPositionIK, GetPositionIKRequest, GetPositionIKResponse
from baxter_interface import gripper as robot_gripper
from geometry_msgs.msg import PoseStamped
from moveit_commander import MoveGroupCommander
import numpy as np
from numpy import linalg

def main():
    startX, startY, startZ = 0.846, 0.215, -0.161
    endX, endY, endZ = 0.794, 0.014, -0.149
    
    #Wait for the IK service to become available
    rospy.wait_for_service('compute_ik')
    rospy.init_node('service_query')

    left_gripper = robot_gripper.Gripper('left')
    #Calibrate the gripper (other commands won't work unless you do this first)
    print('Calibrating left gripper...')
    left_gripper.calibrate()
    rospy.sleep(2.0)
    
    while not rospy.is_shutdown():
        raw_input('Press [ Enter ]: ')
        
        move_to(startX, startY, startZ)
        #Close the right gripper
        print('Closing gripper...')
        left_gripper.close()
        rospy.sleep(1.0)

        move_to(endX, endY, endZ)
        #Open the right gripper
        print('Opening left gripper...')
        left_gripper.open()
        rospy.sleep(1.0)
        print('Done!')

def move_to(x, y, z):
    #Create the function used to call the service
    compute_ik = rospy.ServiceProxy('compute_ik', GetPositionIK)

    #Construct the request
    request = GetPositionIKRequest()
    request.ik_request.group_name = "left_arm"
    request.ik_request.ik_link_name = "left_gripper"
    request.ik_request.attempts = 20
    request.ik_request.pose_stamped.header.frame_id = "base"
    #Set the desired orientation for the end effector HERE
    request.ik_request.pose_stamped.pose.position.x = x
    request.ik_request.pose_stamped.pose.position.y = y
    request.ik_request.pose_stamped.pose.position.z = z     
    request.ik_request.pose_stamped.pose.orientation.x = 0.0
    request.ik_request.pose_stamped.pose.orientation.y = 1.0
    request.ik_request.pose_stamped.pose.orientation.z = 0.0
    request.ik_request.pose_stamped.pose.orientation.w = 0.0
    
    try:
        #Send the request to the service
        response = compute_ik(request)
        
        #Print the response HERE
        print(response)
        group = MoveGroupCommander("left_arm")

        # Setting position and orientation target
        group.set_pose_target(request.ik_request.pose_stamped)

        # TRY THIS
        # Setting just the position without specifying the orientation
        ###group.set_position_target([0.5, 0.5, 0.0])

        # Plan IK and execute
        group.go()
        
    except rospy.ServiceException, e:
        print "Service call failed: %s"%e

#Python's syntax for a main() method
if __name__ == '__main__':
    main()

