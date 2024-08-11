#!/usr/bin/env python3

import rospy
from geometry_msgs.msg import Twist
from sensor_msgs.msg import LaserScan

class RobotNavigation():
    def __init__(self):
        rospy.init_node('robot_navigation', anonymous=True)
        
        self.cmd_vel_publisher = rospy.Publisher('/cmd_vel', Twist, queue_size=1)
        
        # Üç lazer sensörü için subscriber
        self.front_laser_subscriber = rospy.Subscriber('/base_scan_0', LaserScan, self.front_laser_callback, queue_size=1)
        self.left_laser_subscriber = rospy.Subscriber('/base_scan_1', LaserScan, self.left_laser_callback, queue_size=1)
        self.right_laser_subscriber = rospy.Subscriber('/base_scan_2', LaserScan, self.right_laser_callback, queue_size=1)
        
        # Lazer verileri için değişkenler
        self.front_distance = float('inf')
        self.left_distance = float('inf')
        self.right_distance = float('inf')
        
        self.obstacle_distance = 0.8  
        self.limit_distance = 0.6
        self.min_distance= 0.3
        self.rate = rospy.Rate(5)  
        self.cmd_vel = Twist()

    def front_laser_callback(self, data):
        self.front_distance = min(data.ranges)

    def left_laser_callback(self, data):
        self.left_distance = min(data.ranges)

    def right_laser_callback(self, data):
        self.right_distance = min(data.ranges)

    def move_forward(self):
        self.cmd_vel.linear.x = 0.4  
        self.cmd_vel.angular.z = 0.0  
        self.cmd_vel_publisher.publish(self.cmd_vel)

    def move_backward(self):
        self.cmd_vel.linear.x = -0.2  
        self.cmd_vel.angular.z = 0.0  
        self.cmd_vel_publisher.publish(self.cmd_vel)

    def slight_left(self):
        self.cmd_vel.linear.x = 0.1
        self.cmd_vel.angular.z = 0.2
        self.cmd_vel_publisher.publish(self.cmd_vel)

    def slight_right(self):
        self.cmd_vel.linear.x = 0.1
        self.cmd_vel.angular.z = -0.2
        self.cmd_vel_publisher.publish(self.cmd_vel)

        
    def follow_wall(self):    

    
        if self.front_distance < self.obstacle_distance:
            self.slight_left()
        else:
            if self.right_distance < self.min_distance:
                self.slight_left()
            elif self.right_distance > self.limit_distance:
                self.slight_right()
            else:
                self.move_forward()
            


    def run(self):
        while not rospy.is_shutdown():
            self.follow_wall()
            self.rate.sleep()

if __name__ == '__main__':
        robot_nav = RobotNavigation()
        robot_nav.run()
