#!/bin/bash
source /opt/ros/foxy/setup.bash
export TURTLEBOT3_MODEL=burger
export ROS_DOMAIN_ID=30

trap "trap - SIGTERM && kill -- -$$" SIGINT SIGTERM EXIT

ros2 launch turtlebot3_gazebo turtlebot3_world.launch.py &
sudo docker build --build-arg base="ros:foxy" -t turtlebotfoxy . && sudo docker run -it turtlebotfoxy

