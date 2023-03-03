# FROM arm64v8/ros:foxy
ARG base=arm64v8/ros:foxy
FROM $base
ENV DEBIAN_FRONTEND=noninteractive 

SHELL ["/bin/bash", "-c"]

RUN apt-get update && apt-get -y upgrade
RUN apt-get install -y net-tools

ADD /ros2_basics /ros2_basics

RUN source ~/.bashrc
RUN source /opt/ros/foxy/setup.bash

ENV ROS_DOMAIN_ID=30
ENV export TURTLEBOT3_MODEL=burger

RUN cd ros2_basics/cpp_topic && rosdep install -i --from-path src --rosdistro foxy -y
RUN . /opt/ros/foxy/setup.sh &&\
    cd ros2_basics/cpp_topic && colcon build --packages-select cpp_topic

CMD cd ros2_basics/cpp_topic && . install/setup.bash &&\
    ros2 run cpp_topic cpp_topic_publisher_spiral

ENTRYPOINT ["/ros_entrypoint.sh"]

####################################################

###ROS CONTROLLEUR:
#necessite docker sur pc
# sudo docker build --build-arg base="ros:foxy" -t turtlebotfoxy .
# sudo docker run -it turtlebotfoxy

###SIMULATION:
#necessite ros2, gazebo et packages (https://emanual.robotis.com/docs/en/platform/turtlebot3/simulation/#gazebo-simulation)
# source /opt/ros/foxy/setup.bash
# source ~/.bashrc
# export TURTLEBOT3_MODEL=burger
# export ROS_DOMAIN_ID=30
# ros2 launch turtlebot3_gazebo turtlebot3_house.launch.py
#sudo docker run --net=host -it --rm  matthisdockers/test:latest /bin/bash