#include <ros/ros.h>  
#include <tf/transform_broadcaster.h>
#include <nav_msgs/Odometry.h>
#include <gazebo_msgs/ModelStates.h>

double vx =0;
double vy = 0;
double vth = 0;
// 启动时将机器人放稳
double x = 0.0;
double y = 0.0;
geometry_msgs::Quaternion odom_quat;


void callback(const gazebo_msgs::ModelStates model_state){
  vy = model_state.twist[2].linear.y;
  vx = model_state.twist[2].linear.x;
  vth = model_state.twist[2].angular.z;
  x = model_state.pose[2].position.x;
  y = model_state.pose[2].position.y;
  odom_quat = model_state.pose[2].orientation;

}
int main(int argc, char** argv){
  ros::init(argc, argv, "odometry_publisher");

  ros::NodeHandle n;
  ros::Publisher odom_pub = n.advertise<nav_msgs::Odometry>("odom", 50);
  tf::TransformBroadcaster odom_broadcaster;
  ros::Subscriber info_sub = n.subscribe("/gazebo/model_states", 1, callback);
  ros::Time current_time;
  ros::Rate r(800);
  while(n.ok()){

    ros::spinOnce();               // check for incoming messages

    current_time = ros::Time::now();
    //first, we'll publish the transform over tf
    geometry_msgs::TransformStamped odom_trans;
    odom_trans.header.stamp = current_time;
    odom_trans.header.frame_id = "odom";
    odom_trans.child_frame_id = "base_link";

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
    odom.twist.twist.angular.z = vth;

    //publish the message
    odom_pub.publish(odom);

    r.sleep();
  }
}