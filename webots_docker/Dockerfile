FROM cyberbotics/webots
ENV DEBIAN_FRONTEND=noninteractive
ENV DISPLAY=host.docker.internal:0.0
SHELL ["/bin/bash", "-c"]
RUN apt-get update && apt-get -y upgrade
CMD webots

#docker build . -t webots
#docker run -it --net=host webots