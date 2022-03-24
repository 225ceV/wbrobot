#!/usr/bin/env python
from control import lqr, ss
import numpy as np
import rospy
from robot_control.srv import Gain, GainResponse      # Gain.srv

class online_lqr_node:
    def __init__(self):
        # 定义机器人的物理属性
        # S1=subs(S,{M m Jw R L Jp Jb D g},{8, 0.10249, 0.00015, 0.05, 0.2100,0.0584,0.0558,0.256,9.8});
        self.M = 8
        self.m = 0.10249
        self.Jw = 0.00015
        self.R = 0.05
        self.L = 0.21 # default
        self.Jp = 0.0584
        self.Jb = 0.0558
        self.D = 0.256
        self.g = 9.8
        self.sys_v = None      # 速度控制系统矩阵
        self.sys_delta = None  # 航向控制系统矩阵

        # lqr权重值
        self.Qv = np.diag([50, 1, 12])
        # self.Qv = np.diag([50, 0, 0])
        self.Rv = np.diag([1])
        self.Qdelta = np.diag([10, 1])
        self.Rdelta = np.diag([1])

        
        rospy.init_node('online_lqr')
        self.server = rospy.Service('/lqr_gain', Gain, self.gainCallBack)
        rospy.loginfo("LQR Optimizer Node is Online...")
        rospy.spin()


    def update_system(self, l):
        # 在高度信息变化时更新系统矩阵
        self.L = l
        M, m, Jw, R, L, Jp, Jb, D, g = self.M, self.m, self.Jw, self.R, self.L, self.Jp, self.Jb, self.D, self.g

        Av = np.array([[0,                -(L**2*M**2*R**2*g)/(2*Jp*Jw + 2*Jw*L**2*M + Jp*M*R**2 + 2*Jp*R**2*m + 2*L**2*M*R**2*m), 0], 
                       [0,                                                                                                      0, 1], 
                       [0, (L*M*g*(2*Jw + M*R**2 + 2*R**2*m))/(2*Jp*Jw + 2*Jw*L**2*M + Jp*M*R**2 + 2*Jp*R**2*m + 2*L**2*M*R**2*m), 0]])
        Bv = np.array([[                                   (Jp*R)/(2*Jp*Jw + 2*Jw*L**2*M + Jp*M*R**2 + 2*Jp*R**2*m + 2*L**2*M*R**2*m) + (L*M*R**2*(L/R + 1))/(2*Jp*Jw + 2*Jw*L**2*M + Jp*M*R**2 + 2*Jp*R**2*m + 2*L**2*M*R**2*m)],
                       [                                                                                                                                                                                                       0],
                       [(2*L*(m*R**2 + Jw))/(R*(2*Jp*Jw + 2*Jw*L**2*M + Jp*M*R**2 + 2*Jp*R**2*m + 2*L**2*M*R**2*m)) - ((L/R + 1)*(2*Jw + M*R**2 + 2*R**2*m))/(2*Jp*Jw + 2*Jw*L**2*M + Jp*M*R**2 + 2*Jp*R**2*m + 2*L**2*M*R**2*m)]])
        print(Av)
        print(Bv)
        Adelta = np.array([[0, 1],
                           [0, 0]])
        Bdelta = np.array([[                                        0], 
                           [(D*R)/(m*D**2*R**2 + Jw*D**2 + 2*Jb*R**2)]])
        print(Adelta)
        print(Bdelta)
        self.sys_v = ss(Av, Bv, np.eye(3), np.zeros((3,1)))
        self.sys_delta = ss(Adelta, Bdelta, np.eye(2), np.zeros((2,1)))

        rospy.loginfo("State Space Model Updated.")

    def gainCallBack(self, req):
        self.update_system(req.l)
        Kv, _, _ = lqr(self.sys_v, self.Qv, self.Rv)
        Kdelta, _, _ = lqr(self.sys_delta, self.Qdelta, self.Rdelta)
        res = GainResponse()
        res.K = Kv.flatten().tolist() + Kdelta.flatten().tolist()
        # res = (Kv.flatten().tolist() + Kdelta.flatten().tolist())
        print(res.K)
        return res


if __name__ == "__main__":
    lqr_node = online_lqr_node()
    # print(lqr_node.gainCallBack(0.04))
