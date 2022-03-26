#!/usr/bin/env python
# 多传感器融合，将多个信号订阅到一个节点并发布
import rospy
import message_filters
# from rosbot3_ctrl.msg import system_K
from robot_control.msg import robot_orientation
from robot_control.msg import multi_info
from sensor_msgs.msg import JointState
from robot_control.msg import cmd

class multi_receive_node:
    def __init__(self):
        rospy.init_node('multi_receive')
        # sys_k_sub = message_filters.Subscriber('/sys_K', system_K)
        robot_orientation_sub = message_filters.Subscriber('/orientation', robot_orientation)
        joint_state_sub = message_filters.Subscriber("/joint_states",JointState)
        cmd_sub = message_filters.Subscriber('/cmd', cmd)
        self.pub = rospy.Publisher('/multi_info', multi_info, queue_size=1)
        # 时间序列处理
        self.ts = message_filters.ApproximateTimeSynchronizer([joint_state_sub, robot_orientation_sub, cmd_sub], 1, 0.1)

        self.ts.registerCallback(self.callback)
        rospy.spin()
    def callback(self, js, ro, c):
        # print('ok') 
        # x1=js.position[2]
        # x2=js.position[3]
        # x=0.5*(x1+x2)
        dx1=js.velocity[2]*0.05
        dx2=js.velocity[3]*0.05
        
        info = multi_info()
        info.dx=0.5*(dx1+dx2)
        info.theta = ro.theta
        info.dtheta = ro.dtheta
        info.delta = ro.delta
        info.ddelta = ro.ddelta
        info.cmd_v = c.cmd_v
        info.cmd_delta = c.cmd_delta
        info.cmd_ddelta = c.cmd_ddelta
        # 时间戳
        info.header.stamp = rospy.Time.now()
        self.pub.publish(info)
        # print(log_msg)


if __name__ == "__main__":
    multi_receive = multi_receive_node()