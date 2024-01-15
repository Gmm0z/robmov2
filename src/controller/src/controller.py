#!/usr/bin/env python
#Pablo José Cremades Garrido  -- Robots Móviles Proyecto. 
import rospy
import actionlib
import cv2
from cv_bridge import CvBridge, CvBridgeError
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal
from sensor_msgs.msg import Image

def send_goal_to_move_base(x, y, theta):
    # Create an action client called "move_base" with action definition file "MoveBaseAction"
    client = actionlib.SimpleActionClient('move_base', MoveBaseAction)
    
    # Waits until the action server has started up and started listening for goals.
    client.wait_for_server()

    # Creates a new goal with the MoveBaseGoal constructor
    goal = MoveBaseGoal()
    goal.target_pose.header.frame_id = "map"
    goal.target_pose.header.stamp = rospy.Time.now()
    
    # Set goal position (x, y) and orientation (theta)
    goal.target_pose.pose.position.x = x
    goal.target_pose.pose.position.y = y
    goal.target_pose.pose.orientation.w = theta

    # Sends the goal to the action server.
    client.send_goal(goal)

    # Waits for the server to finish performing the action.
    wait = client.wait_for_result()

    # If the result doesn't come, continue doing other stuff
    if not wait:
        rospy.logerr("Action server not available!")
    else:
        # Prints out the result of executing the action
        return client.get_result()  # A MoveBaseResult


# Callback function for the camera subscriber
def image_callback(data):
    try:
        cv_image = CvBridge().imgmsg_to_cv2(data, "bgr8")
    except CvBridgeError as e:
        rospy.logerr(e)

    # Display the image
    cv2.imshow("Robot Camera Feed", cv_image)
    cv2.waitKey(3)

if __name__ == '__main__':
    try:
        rospy.init_node('simple_navigation_goals')
        
        # Create a subscriber for the camera topic
        rospy.Subscriber('/camera/rgb/image_raw', Image, image_callback)

        while not rospy.is_shutdown():
            send_goal_to_move_base(0.332333, 1.201825, 1.0) 
            send_goal_to_move_base(-1.141606, -1.970344, 1.0)

    except rospy.ROSInterruptException:
        rospy.loginfo("Navigation test finished.")
    finally:
        cv2.destroyAllWindows()
