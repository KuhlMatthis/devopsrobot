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
CMD ipaddress=$(hostname -i) &&\
    echo "export ROS_MASTER_URI=http://$ipaddress:11311" >> ~/.bashrc &&\
    echo "export ROS_HOSTNAME=$ipaddress" >> ~/.bashrc &&\
    source ros_entrypoint.sh &&\
    source ~/.bashrc &&\
    bash
ENTRYPOINT ["/ros_entrypoint.sh"]

####################################################
###COMMANDES:
#docker build . -t turtlebot
#docker run -it --net=host turtlebot
#containeur 1 terminal 1: roscore 
#containeur 1 terminal 2: rostopic pub -r 1 /my_topic std_msgs/String '{data: "hello"}'
#containeur 2 terminal 1: rostopic echo /my_topic

####################################################
###TODO:
#connecter ce docker avec robot
#lancer programme ros depuis docker pour piloter le robot
#créer dossier contenant le programme ROS et le copier et lancer automatiquement dans le docker
#créer docker traducteur faisant le lien entre docker ROS et Webots tcp/ip
#yaml permettant le lancement de tout d'un coup
#github workflow pour automatiser cette démarche à chaque push
#mettre en avant  l'aspect microservice des controlleurs et rendre leur ajout/modification/suppression dynamique

####################################################