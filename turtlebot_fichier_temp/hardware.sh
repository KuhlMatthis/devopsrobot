#!/bin/bash

echo "Running ros"
(/opt/ros/foxy/bin/ros2 launch turtlebot3_bringup robot.launch.py) &

sleep 10

echo "Running docker conateiner"

/opt/ros/foxy/bin/ros2 topic list
#/opt/ros/foxy/bin/ros2 pub --rate 1 /cmd_vel geometry_msgs/msg/Twist "{linear: {x: 2.0, y: 0.0, z: 0.0}, angular: {x: 0.0, y: 0.0, z: 1.8}}"

/usr/bin/docker run --name mycontainer --rm  matthisdockers/test
echo "Both running"