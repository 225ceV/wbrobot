#!/usr/bin/python3
import rospy
from std_msgs.msg import Float64MultiArray
import numpy as np
from  robot_control.srv import Gain,GainRequest
from robot_control.msg import multi_info

# ro do 将控制指令写成消息， 将多个节点的初始化写成类， 创建git

class v_control_node:
    def __init__(self):
        # self.v = v
        # self.delta = delta
        # self.k1 = k1
        # self.k2 = k2
        rospy.init_node('control_node',anonymous=True)

        self.sub =rospy.Subscriber('/multi_info', multi_info, self.callback)
        self.pub = rospy.Publisher("/joints_effort_controller/command", Float64MultiArray, queue_size=1)
        self.pub2 = rospy.Publisher("/joints_position_controller/command", Float64MultiArray, queue_size=1)

    def callback(self, md):
        x_vec1=np.array([[md.dx],[md.pitch],[md.dpitch]])
        x_vec2=np.array([[md.yaw],[md.dyaw]])
        u1=-k1.dot(x_vec1 - np.array([[0.5],[0],[0]]))
        # u2=-k2.dot(x_vec2 - np.array([[delta], [0]]))
        u2 = 0
        # u1=-k1.dot(x_vec1) + g1.dot(np.array([[v], [0], [0]]))
        # u2=-k2.dot(x_vec2) + g2.dot(np.array([[delta], [0]]))
        Cl=0.5*u1+0.5*u2
        Cr=0.5*u1-0.5*u2
        if np.abs(md.pitch) > np.pi/3:
            Cl = 0
            Cr = 0
        C=Float64MultiArray(data=[Cl,Cr])
        print('ok')
        self.pub.publish(C)

        t1 = np.arcsin(L/2/0.21)
        t2 = 2*t1-25/180*np.pi
        self.pub2.publish(Float64MultiArray(data = [t1, t2, t1, t2]))



if __name__=='__main__':   
    ## 获取k1 k2
    client = rospy.ServiceProxy("/lqr_gain",Gain)
    client.wait_for_service()
    req = GainRequest()
    req.l = 0.21
    L = req.l
    response = client.call(req)
    k1 = np.array(response.K[0:3])
    # k1[0] = 0
    k2 = np.array(response.K[3:])

    g1 = np.array(response.G[0:3])
    # k1[0] = 0
    g2 = np.array(response.G[3:])
    print(k1)

    v = 0.5
    delta = 1.57
    v_controller = v_control_node()
    rospy.spin()