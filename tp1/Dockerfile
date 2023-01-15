FROM ros:noetic
ENV DEBIAN_FRONTEND=noninteractive
SHELL ["/bin/bash", "-c"]
RUN apt-get update && apt-get -y upgrade
RUN apt-get install -y net-tools
# install the needed packages for the ros master for the turtlebot burger 3
RUN apt-get install -y ros-noetic-joy ros-noetic-teleop-twist-joy \
    ros-noetic-teleop-twist-keyboard ros-noetic-laser-proc \
    ros-noetic-rgbd-launch ros-noetic-rosserial-arduino \
    ros-noetic-rosserial-python ros-noetic-rosserial-client \
    ros-noetic-rosserial-msgs ros-noetic-amcl ros-noetic-map-server \
    ros-noetic-move-base ros-noetic-urdf ros-noetic-xacro \
    ros-noetic-compressed-image-transport ros-noetic-rqt* ros-noetic-rviz \
    ros-noetic-gmapping ros-noetic-navigation ros-noetic-interactive-markers \
    ros-noetic-dynamixel-sdk ros-noetic-turtlebot3-msgs ros-noetic-turtlebot3
# doesn't work yet, this is giving the compter's ip instead of the container's
RUN ipaddress=$(hostname -i) &&\
    echo "export ROS_MASTER_URI=http://$ipaddress:11311" >> ~/.bashrc &&\
    echo "export ROS_HOSTNAME=$ipaddress" >> ~/.bashrc &&\
    source ~/.bashrc
ENTRYPOINT ["/ros_entrypoint.sh"]

#docker build . -t turtlebot
#docker run -it -d --name turtle turtlebot bash

#start ros container with ros master active:
#docker run -it --net=host turtlebot roscore
#start ros container (new terminal):
#docker run -it --net=host turtlebot bash
#rostopic list dans le bash pour voir les topic