#!/usr/bin/python3
import rospy
from sensor_msgs.msg import Imu
from robot_control.msg import robot_orientation
import math

class imu_do_node:
    def __init__(self):
        rospy.init_node('imu_do_node',anonymous=True)
        self.pub = rospy.Publisher('/orientation', robot_orientation, queue_size=1)
        self.sub =rospy.Subscriber("/imu",Imu,self.imu_get)
        rospy.spin()
    def imu_get(self, imu_data):
        o = robot_orientation()
        '''x = float(imu_data.orientation.x) #q1
        y = float(imu_data.orientation.y) #q2
        z = float(imu_data.orientation.z) #q3
        w = float(imu_data.orientation.w) #q0
        o.pitch = - math.atan2(2*(w*x+y*z),1-2*(x**2+y**2))
        o.yaw = math.atan2(2*(w*z+x*y),1-2*(y**2+z**2))'''
        q1 = float(imu_data.orientation.x) #q1
        q2 = float(imu_data.orientation.y) #q2
        q3 = float(imu_data.orientation.z) #q3
        q0 = float(imu_data.orientation.w) #q0
        
        
        ry0 = 2*(q1*q2-q0*q3)
        ry1 = 1-2*(q1*q1+q3*q3)
        ry2 = 2*(q2*q3+q0*q1)
        
        o.pitch=math.atan(-ry2/math.sqrt(ry0**2+ry1**2))
        o.yaw=math.atan(ry0/math.sqrt(ry1**2+ry2**2))
        
        o.dpitch=-imu_data.angular_velocity.x
        o.dyaw=-imu_data.angular_velocity.z
        # 时间戳
        o.header.stamp = rospy.Time.now()
        # 发布
        # print(ry0)
        self.pub.publish(o)


if __name__ == "__main__":
    imu = imu_do_node()