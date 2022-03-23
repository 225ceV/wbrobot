#!/usr/bin/env python
# 多传感器融合，将多个信号订阅到一个节点并发布
import rospy
import numpy as np
import message_filters
# from rosbot3_ctrl.msg import system_K
from robot_control.msg import robot_orientation
from robot_control.msg import multi_info
from std_msgs.msg import Float64MultiArray
from sensor_msgs.msg import JointState


def callback(js, ro):
    # print('ok') 
    # x1=js.position[2]
    # x2=js.position[3]
    # x=0.5*(x1+x2)
    dx1=js.velocity[2]*0.05
    dx2=js.velocity[3]*0.05
    
    info = multi_info()
    info.dx=0.5*(dx1+dx2)
    info.pitch = ro.pitch
    info.dpitch = ro.dpitch
    info.yaw = ro.yaw
    info.dyaw = ro.dyaw
    # 时间戳
    info.header.stamp = rospy.Time.now()
    pub.publish(info)
    # print(log_msg)


if __name__ == "__main__":
    rospy.init_node('multi_receive')
    # sys_k_sub = message_filters.Subscriber('/sys_K', system_K)
    robot_orientation_sub = message_filters.Subscriber('/orientation', robot_orientation)
    joint_state_sub = message_filters.Subscriber("/joint_states",JointState)
    pub = rospy.Publisher('/multi_info', multi_info, queue_size=1)
    # 时间序列处理
    ts = message_filters.ApproximateTimeSynchronizer([joint_state_sub, robot_orientation_sub], 1, 0.1)

    ts.registerCallback(callback)
    rospy.spin()