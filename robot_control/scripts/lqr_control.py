#!/usr/bin/python3
import rospy
# from sensor_msgs.msg import Imu
# from sensor_msgs.msg import JointState
# from std_msgs.msg import MultiArrayLayout
from std_msgs.msg import Float64MultiArray
import math
import numpy as np
from  robot_control.srv import Gain,GainRequest
from robot_control.msg import multi_info

def callback(md):
    x_vec1=np.array([[md.dx],[md.pitch],[md.dpitch]])
    x_vec2=np.array([[md.yaw],[md.dyaw]])
    u1=-k1.dot(x_vec1-np.array([[0.5],[0],[0]]))
    # u1=-k1.dot(x_vec1)
    u2=-k2.dot(x_vec2)
    Cl=0.5*u1+0.5*u2
    Cr=0.5*u1-0.5*u2
    if np.abs(md.pitch) > np.pi/3:
        Cl = 0
        Cr = 0
    C=Float64MultiArray(data=[Cl,Cr])
    # print('ok')
    pub.publish(C)

    t = np.arcsin(L/2/0.21)
    t1 = t - 12.5/180*np.pi
    t2 = 2*t-25/180*np.pi
    pub2.publish(Float64MultiArray(data = [t1, t2, t1, t2]))


if __name__=='__main__':
    # global x,dx,pitch,dpitch,yaw,dyaw,x_vec1,x_vec2,k1,k2
    rospy.init_node('control_node',anonymous=True)
    ## 获取k1 k2
    client = rospy.ServiceProxy("/lqr_gain",Gain)
    client.wait_for_service()
    req = GainRequest()
    req.l = 0.08
    L = req.l
    response = client.call(req)
    k1 = np.array(response.K[0:3])
    # k1[0] = 0
    k2 = np.array(response.K[3:])
    print(k1)
    ## 获取imu信息
    sub =rospy.Subscriber('/multi_info', multi_info, callback)
    pub = rospy.Publisher("/joints_effort_controller/command", Float64MultiArray, queue_size=1)

    pub2 = rospy.Publisher("/joints_position_controller/command", Float64MultiArray, queue_size=1)

    du5 = rospy.Duration(10)
    rospy.sleep(du5)

    req.l = 0.21
    L = req.l
    response = client.call(req)
    k1 = np.array(response.K[0:3])
    # k1[0] = 0
    k2 = np.array(response.K[3:])


    rospy.spin()