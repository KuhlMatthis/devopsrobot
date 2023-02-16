FROM ros:foxy
ENV DEBIAN_FRONTEND=noninteractive

SHELL ["/bin/bash", "-c"]

RUN apt-get update && apt-get -y upgrade
RUN apt-get install -y net-tools

# install the needed packages for the ros master for the turtlebot burger 3
RUN apt-get install -y ros-foxy-gazebo-* ros-foxy-cartographer ros-foxy-cartographer-ros \
    ros-foxy-navigation2 ros-foxy-nav2-bringup
RUN source ~/.bashrc
RUN apt-get install -y ros-foxy-dynamixel-sdk ros-foxy-turtlebot3-msgs ros-foxy-turtlebot3
RUN apt-get install -y ros-foxy-turtlebot3-gazebo

ENV ROS_DOMAIN_ID=30
ENV export TURTLEBOT3_MODEL=burger

CMD ros2 run turtlebot3_gazebo turtlebot3_drive
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