#!/usr/bin/env python  
# -*- coding: utf-8 -*  
  
import  os  
import  sys  
import  tty, termios

from matplotlib import offsetbox  
import rospy  
from robot_control.msg import cmd
from std_msgs.msg import String  
from cmd_node import cmd_node
  

# 不论用cpp还是python 直接读取键盘的频率不够
# 全局变量  

  
def keyboardLoop():  
    #速度变量  
    walk_vel_ = 0.2
    run_vel_ = 0.5
    yaw_rate_ = 0.5  
    yaw_rate_run_ = 1  
  
    max_tv = walk_vel_  
    max_rv = yaw_rate_  
  
    #显示提示信息  
    print("Reading from keyboard") 
    print("Use QWEASDZXC keys to control the robot") 
    print("Press Caps to move faster")  
    print("Press b to quit")  
  
    #读取按键循环  
    while not rospy.is_shutdown():  
        fd = sys.stdin.fileno()  
        old_settings = termios.tcgetattr(fd)  
        #不产生回显效果  
        old_settings[3] = old_settings[3] & ~termios.ICANON & ~termios.ECHO  
        try :  
            tty.setraw( fd )  
            ch = sys.stdin.read( 1 )  
        finally :  
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)  
  
        if ch == 'w':  
            max_tv = walk_vel_  
            speed = 1  
            turn = 0  
        elif ch == 'W':  
            max_tv = run_vel_  
            speed = 1  
            turn = 0  
        elif ch == 's':  
            max_tv = walk_vel_  
            speed = 0
            turn = 0  
        elif ch == 'S':  
            max_tv = run_vel_  
            speed = 0
            turn = 0  
        elif ch == 'a':  
            max_rv = yaw_rate_  
            speed = 0  
            turn = 1  
        elif ch == 'A':  
            max_rv = yaw_rate_run_  
            speed = 0  
            turn = 1  
        elif ch == 'd':  
            max_rv = yaw_rate_  
            speed = 0  
            turn = -1     
        elif ch == 'D':  
            max_rv = yaw_rate_run_  
            speed = 0  
            turn = -1  
        elif ch == 'e':  
            max_rv = yaw_rate_
            speed = 1  
            turn =  -1
        elif ch == 'E':  
            max_rv = yaw_rate_run_  
            speed = 1
            turn =  -1
        elif ch == 'q':  
            max_rv = yaw_rate_
            max_tv = walk_vel_  
            speed = 1  
            turn =  1
        elif ch == 'Q':  
            max_rv = yaw_rate_run_
            max_tv = run_vel_  
            speed = 1  
            turn =  1
        elif ch == 'z':  
            max_rv = yaw_rate_
            max_tv = walk_vel_  
            speed = -1  
            turn =  -1
        elif ch == 'Z':  
            max_rv = yaw_rate_run_
            max_tv = run_vel_  
            speed = -1  
            turn =  -1
        elif ch == 'x':  
            max_rv = yaw_rate_
            max_tv = walk_vel_  
            speed = -1  
            turn =  0
        elif ch == 'X':  
            max_rv = yaw_rate_run_
            max_tv = run_vel_  
            speed = -1  
            turn =  0
        elif ch == 'z':  
            max_rv = yaw_rate_
            max_tv = walk_vel_  
            speed = -1  
            turn =  1
        elif ch == 'Z':  
            max_rv = yaw_rate_run_
            max_tv = run_vel_  
            speed = -1  
            turn =  1
        elif ch == 'b':  
            exit()  
        else:  
            max_tv = walk_vel_  
            max_rv = yaw_rate_  
            speed = 0  
            turn = 0  
  
        #发送消息  
        off_set = 0.095
        rospy.set_param('tv', max_tv*speed+off_set)
        rospy.set_param('rv', -max_rv*turn)
  

  
if __name__ == '__main__':  
    keyboardLoop()  
