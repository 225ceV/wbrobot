#! usr/bin/env python

import rospy
import numpy as np
from robot_control.srv import Gain,GainRequest
from robot_control.msg import system_K


    ## 获取k1 k2
rospy.init_node('k_pub')

pub = rospy.Publisher('/sys_K', system_K, queue_size=1, latch=True) # 锁存消息
client = rospy.ServiceProxy("/lqr_gain",Gain)
client.wait_for_service()

req = GainRequest()
req.l = 0.21

K = system_K()

response = client.call(req)
print(response)
K.kv = np.array(response.K[0:3])
K.kdelta = np.array(response.K[3:])

rate = rospy.Rate(10)
while not rospy.is_shutdown:
    print('ok')
    pub.publish(K)
    rate.sleep()