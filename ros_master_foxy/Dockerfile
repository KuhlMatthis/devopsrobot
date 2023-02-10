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
CMD echo 'export ROS_DOMAIN_ID=30 #TURTLEBOT3' >> ~/.bashrc &&\
    source ros_entrypoint.sh &&\
    source ~/.bashrc &&\
    bash
ENTRYPOINT ["/ros_entrypoint.sh"]

####################################################

###COMMANDES:
#docker build . -t turtlebotfoxy
#docker run -it --net=host turtlebotfoxy
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