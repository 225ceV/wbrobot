#!/usr/bin/python3
import rospy
from robot_control.msg import cmd

class cmd_node:
    def __init__(self):
        rospy.init_node('cmd_node')
        self.pub = rospy.Publisher('/cmd', cmd, queue_size=1)
        self.rate = rospy.Rate(800)
    def move(self, v, delta, duration):
        cmd_msg = cmd()
        cmd_msg.cmd_v = v
        cmd_msg.cmd_delta = delta
        start = rospy.Time.now()
        while rospy.Time.now() < start + rospy.Duration(duration):
            cmd_msg.header.stamp = rospy.Time.now()
            self.pub.publish(cmd_msg)
            self.rate.sleep()
    def stand(self, duration):
        cmd_msg = cmd() 
        cmd_msg.cmd_v = 0.095      # lqr 控制器的系统偏差
        cmd_msg.cmd_delta = 0
        start = rospy.Time.now()
        while rospy.Time.now() < start + rospy.Duration(duration):
            cmd_msg.header.stamp = rospy.Time.now()
            self.pub.publish(cmd_msg)
            self.rate.sleep()
if __name__ == "__main__":
    cmd_pub = cmd_node()
    cmd_pub.stand(5)
    cmd_pub.move(0.2, 0, 3)
    cmd_pub.move(0.5, 0, 3)
    cmd_pub.move(0.5, 1.05, 3)
    cmd_pub.move(0.5, 0, 3)
    cmd_pub.move(0.5, -1.05, 3)
    cmd_pub.move(0.5, 0, 3)