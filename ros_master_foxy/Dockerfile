FROM ros:foxy
ENV DEBIAN_FRONTEND=noninteractive

SHELL ["/bin/bash", "-c"]

RUN apt-get update && apt-get -y upgrade
RUN apt-get install -y net-tools

ADD /ros2_basics /ros2_basics

# install the needed packages for the ros master for the turtlebot burger 3
#RUN source ~/.bashrc
#RUN apt-get install -y ros-foxy-turtlebot3-gazebo

ENV ROS_DOMAIN_ID=30
ENV export TURTLEBOT3_MODEL=burger

RUN cd /ros2_basics/cpp_topic &&\ 
    rosdep install -i --from-path src --rosdistro foxy -y &&\
    colcon build --packages-select cpp_topic &&\
    . install/setup.bash

CMD ros2 run cpp_topic cpp_topic_publisher_spiral
ENTRYPOINT ["/ros_entrypoint.sh"]

####################################################

###ROS CONTROLLEUR:
#necessite docker sur pc
# sudo docker build . -t turtlebotfoxy
# sudo docker run -it turtlebotfoxy

###SIMULATION:
#necessite ros2, gazebo et packages (https://emanual.robotis.com/docs/en/platform/turtlebot3/simulation/#gazebo-simulation)
# source /opt/ros/foxy/setup.bash
# source ~/.bashrc
# export TURTLEBOT3_MODEL=burger
# export ROS_DOMAIN_ID=30
# ros2 launch turtlebot3_gazebo turtlebot3_house.launch.py