#!/usr/bin/env python3
import numpy as np
import rospy

from robot_control.srv import Gain, GainRequest, GainResponse

if __name__ == "__main__":
    rospy.init_node('test_client')
    client = rospy.ServiceProxy("/lqr_gain",Gain)
    client.wait_for_service()
    req = GainRequest()
    req.l = 0.21
    print(req)
    response = client.call(req)

    rospy.loginfo("Kv = {}, Kdelta = {}".format(np.array(response.K[0:3]), np.array(response.K[3:])))

