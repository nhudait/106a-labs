#!/usr/bin/env python
import roslib; roslib.load_manifest('planning')

import rospy
import sys
import actionlib
from moveit_msgs.msg import MoveGroupAction, MoveGroupGoal, MoveGroupFeedback, MoveGroupResult, JointConstraint, Constraints

def main():
    start_head_pan = float(sys.argv[1])
    start_left_s0 = float(sys.argv[2])
    start_left_s1 = float(sys.argv[3])
    start_left_e0 = float(sys.argv[4])
    start_left_e1 = float(sys.argv[5])
    start_left_w0 = float(sys.argv[6])
    start_left_w1 = float(sys.argv[7])
    start_left_w2 = float(sys.argv[8])
    start_right_s0 = float(sys.argv[9])
    start_right_s1 = float(sys.argv[10])
    start_right_e0 = float(sys.argv[11])
    start_right_e1 = float(sys.argv[12])
    start_right_w0 = float(sys.argv[13])
    start_right_w1 = float(sys.argv[14])
    start_right_w2 = float(sys.argv[15])

    target_head_pan = float(sys.argv[16])
    target_left_s0 = float(sys.argv[17])
    target_left_s1 = float(sys.argv[18])
    target_left_e0 = float(sys.argv[19])
    target_left_e1 = float(sys.argv[20])
    target_left_w0 = float(sys.argv[21])
    target_left_w1 = float(sys.argv[22])
    target_left_w2 = float(sys.argv[23])
    target_right_s0 = float(sys.argv[24])
    target_right_s1 = float(sys.argv[25])
    target_right_e0 = float(sys.argv[26])
    target_right_e1 = float(sys.argv[27])
    target_right_w0 = float(sys.argv[28])
    target_right_w1 = float(sys.argv[29])
    target_right_w2 = float(sys.argv[30])

    #Initialize the node
    rospy.init_node('moveit_client')
    
    # Create the SimpleActionClient, passing the type of the action
    # (MoveGroupAction) to the constructor.
    client = actionlib.SimpleActionClient('move_group', MoveGroupAction)

    # Wait until the action server has started up and started
    # listening for goals.
    client.wait_for_server()

    # Creates a goal to send to the action server.
    goal = MoveGroupGoal()
    
    #----------------Construct the goal message (start)----------------
    joint_names = ['head_pan', 'left_s0', 'left_s1', 'left_e0', 'left_e1', 'left_w0', 'left_w1', 'left_w2', 'right_s0', 'right_s1', 'right_e0', 'right_e1', 'right_w0', 'right_w1', 'right_w2']
    
    #Set parameters for the planner    
    goal.request.group_name = 'both_arms'
    goal.request.num_planning_attempts = 1
    goal.request.allowed_planning_time = 5.0
    
    #Define the workspace in which the planner will search for solutions
    goal.request.workspace_parameters.min_corner.x = -1
    goal.request.workspace_parameters.min_corner.y = -1
    goal.request.workspace_parameters.min_corner.z = -1
    goal.request.workspace_parameters.max_corner.x = 1
    goal.request.workspace_parameters.max_corner.y = 1
    goal.request.workspace_parameters.max_corner.z = 1
    
    goal.request.start_state.joint_state.header.frame_id = "base"
    
    #Set the start state for the trajectory
    goal.request.start_state.joint_state.name = joint_names
    goal.request.start_state.joint_state.position = [start_head_pan, start_left_s0, start_left_s1, start_left_e0, start_left_e1, start_left_w0, start_left_w1, start_left_w2, start_right_s0, start_right_s1, start_right_e0, start_right_e1, start_right_w0, start_right_w1, start_right_w2]
    goal.request.start_state.joint_state.velocity = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
    
    #Tell MoveIt whether to execute the trajectory after planning it
    goal.planning_options.plan_only = True
    
    #Set the goal position of the robot
    #Note that the goal is specified with a collection of individual
    #joint constraints, rather than a vector of joint angles
    arm_joint_names = joint_names[1:]
    target_joint_angles = [target_head_pan, target_left_s0, target_left_s1, target_left_e0, target_left_e1, target_left_w0, target_left_w1, target_left_w2, target_right_s0, target_right_s1, target_right_e0, target_right_e1, target_right_w0, target_right_w1, target_right_w2]
    tolerance = 0.0001
    consts = []
    for i in range(len(arm_joint_names)):
        const = JointConstraint()
        const.joint_name = arm_joint_names[i]
        const.position = target_joint_angles[i]
        const.tolerance_above = tolerance
        const.tolerance_below = tolerance
        const.weight = 1.0
        consts.append(const)
        
    goal.request.goal_constraints.append(Constraints(name='', joint_constraints=consts))
    #---------------Construct the goal message (end)-----------------

    # Send the goal to the action server.
    client.send_goal(goal)

    # Wait for the server to finish performing the action.
    client.wait_for_result()

    # Print out the result of executing the action
    print(client.get_result())
    

if __name__ == '__main__':
    main()

