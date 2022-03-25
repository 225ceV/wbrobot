#!/usr/bin/python3
import rospy
from sensor_msgs.msg import Imu
from robot_control.msg import robot_orientation
import math
import modern_robotics as mr
import numpy as np

class imu_do_node:
    def __init__(self):
        rospy.init_node('imu_do_node',anonymous=True)
        self.pub = rospy.Publisher('/orientation', robot_orientation, queue_size=1)
        self.sub =rospy.Subscriber("/imu",Imu,self.imu_get)
        rospy.loginfo("imu_do_node ok")
        rospy.spin()
    def imu_get(self, imu_data):
        o = robot_orientation()

        '''q1 = float(imu_data.orientation.x) #q1
        q2 = float(imu_data.orientation.y) #q2
        q3 = float(imu_data.orientation.z) #q3
        q0 = float(imu_data.orientation.w) #q0
        
        
        ry0 = 2*(q1*q2-q0*q3)
        ry1 = 1-2*(q1*q1+q3*q3)
        ry2 = 2*(q2*q3+q0*q1)
        
        o.theta=math.atan2(-ry2, math.sqrt(ry0**2+ry1**2))
        o.delta=math.atan2(ry0, math.sqrt(ry1**2+ry2**2))
        
        o.dtheta=-imu_data.angular_velocity.x
        o.ddelta=-imu_data.angular_velocity.z'''
        x = imu_data.orientation.x
        y = imu_data.orientation.y
        z = imu_data.orientation.z
        w = imu_data.orientation.w

        o.theta = - math.atan2(2 * (w * x + y * z), 1 - 2 * (x**2 + y**2))
        o.delta = - math.atan2(2 * (w * z + x * y), 1 - 2 * (y**2 + z**2))
        o.dtheta=-imu_data.angular_velocity.x
        o.ddelta=-imu_data.angular_velocity.z

        """x = float(imu_data.orientation.x) #q1
        y = float(imu_data.orientation.y) #q2
        z = float(imu_data.orientation.z) #q3
        w = float(imu_data.orientation.w) #q0

        angle = np.arccos(w) * 2
        temp = np.sin(angle/2)
        kx = x / temp
        ky = y / temp
        kz = z / temp
        so3mat = mr.VecToso3(np.array([kx, ky, kz])*angle)
        R = mr.MatrixExp3(so3mat)

        ry0 = R[0,1]
        ry1 = R[1,1]
        ry2 = R[2,1]
        
        o.theta=math.atan2(-ry2, math.sqrt(ry0**2+ry1**2))
        o.delta=math.atan2(ry0, math.sqrt(ry1**2+ry2**2))
        ws = np.array([[imu_data.angular_velocity.x], [imu_data.angular_velocity.y], [imu_data.angular_velocity.z]])
        wb = R.T.dot(ws)

        o.dtheta = -wb[0,0]
        o.ddelta = -wb[2,0]"""
        # rospy.loginfo(o.dtheta)
        # 时间戳
        o.header.stamp = rospy.Time.now()
        # 发布
        # print([ry0, ry1, ry2])
        # print(o.delta)
        self.pub.publish(o)


if __name__ == "__main__":
    imu = imu_do_node()