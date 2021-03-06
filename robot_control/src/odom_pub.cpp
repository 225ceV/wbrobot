#include <ros/ros.h>  
#include <tf/transform_broadcaster.h>
#include <nav_msgs/Odometry.h>
#include <robot_control/multi_info.h>  

//odom坐标系的默认前进方向是x轴(rviz) 机器人的前进方向指向y轴(gazebo)
//改tf和th发布, 并加入了base_footprint关节
double v = 0;
double vx =0;
double vy =0;

double vth = 0;
// 启动时将机器人放稳
double x = 0.0;
double y = 0.0;
double th = 0.0;
double th1 = 0.0;
double th2 = 0.0;

void callback(const robot_control::multi_info info){
  v = info.dx;
  vth = info.ddelta;
  th1 = info.delta;
}
int main(int argc, char** argv){
  ros::init(argc, argv, "odometry_publisher");

  ros::NodeHandle n;
  ros::Publisher odom_pub = n.advertise<nav_msgs::Odometry>("odom", 50);
  tf::TransformBroadcaster odom_broadcaster;
  ros::Subscriber info_sub = n.subscribe("multi_info", 1, callback);

  ros::Time current_time, last_time;
  current_time = ros::Time::now();
  last_time = ros::Time::now();

  ros::Rate r(800);
  while(n.ok()){

    ros::spinOnce();               // check for incoming messages
    current_time = ros::Time::now();

    //compute odometry in a typical way given the velocities of the robot
    double dt = (current_time - last_time).toSec();
    double delta_x = v * cos(th) * dt;
    double delta_y = - v * sin(th) * dt;
    double delta_th = vth * dt;
    vx = v * cos(th);
    vy = - v * sin(th);
    x += delta_x;
    y += delta_y;
    th2 += delta_th;
    if(th2>3.14){
      th2-=3.14;
    }else if(th2<-3.14){
      th2+=3.14;
    }
    th = th1;


    //since all odometry is 6DOF we'll need a quaternion created from yaw
    geometry_msgs::Quaternion odom_quat = tf::createQuaternionMsgFromYaw(-th);

    //first, we'll publish the transform over tf
    geometry_msgs::TransformStamped odom_trans;
    odom_trans.header.stamp = current_time;
    odom_trans.header.frame_id = "odom";
    odom_trans.child_frame_id = "base_footprint";

    odom_trans.transform.translation.x = x;
    odom_trans.transform.translation.y = y;
    odom_trans.transform.translation.z = 0.0;
    odom_trans.transform.rotation = odom_quat;

    //send the transform
    odom_broadcaster.sendTransform(odom_trans);

    //next, we'll publish the odometry message over ROS
    nav_msgs::Odometry odom;
    odom.header.stamp = current_time;
    odom.header.frame_id = "odom";

    //set the position
    odom.pose.pose.position.x = x;
    odom.pose.pose.position.y = y;
    odom.pose.pose.position.z = 0.0;
    odom.pose.pose.orientation = odom_quat;

    //set the velocity
    odom.child_frame_id = "base_link";
    odom.twist.twist.linear.x = vx;
    odom.twist.twist.linear.y = vy;
    odom.twist.twist.angular.z = -vth;

    //publish the message
    odom_pub.publish(odom);

    last_time = current_time;
    r.sleep();
  }
}