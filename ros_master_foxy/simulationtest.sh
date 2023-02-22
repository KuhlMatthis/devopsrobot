#! /bin/bash
/bin/bash -c 'ros2 launch turtlebot3_gazebo turtlebot3_world.launch.py &'
/bin/bash -c 'sudo docker build --build-arg base="ros:foxy" -t turtlebotfoxy . && sudo docker run -it turtlebotfoxy'