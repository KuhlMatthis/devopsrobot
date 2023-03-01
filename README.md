# Devops dans la robotique


## Partie turtlebot:

##  Utilisation de l'Image

Vous pouvez récuperer l'image de la carte raspberry du turtlebot utiliser dans notre projet
à l'adresse suivant:  https://drive.google.com/file/d/131MRJGBEvVxsQqDuKMeZVtstDKENaFzl/view.
Cette image à l'avantage d'avoir d'étre exactement l'etat actuelle de notre projet.
Puis avec outil préferer le charger sur le robot:
Dans notre cas nous utilisant Pi Imager c'est l'utile le plus récent est très simple d'utlisation.
Il y a juste à charger directment le fichier zip de l'image télécharger puis séléctioner la carte et clické sur write.
Les options spécifique sur cette image ne vous serrons dans le cas actuelle d'aucune utilité puisque non implementé sur l'image de base de turtlebot.

Lorsque l'image est charger sur la carte ssd vous pouvez lancé le robot.
Avec docker ps vous devriez apercevoir un contenaire docker tourné c'est le conteneur ros final de votre projet.
La toute premiere fois je vous pris de lancé :

```BASH
docker run -d \
    --name watchtower \
    --restart unless-stopped \
    -v /var/run/docker.sock:/var/run/docker.sock \
    containrrr/watchtower -c \
    --interval 3600
```

watchtower est un conteneur permettant de mettre automatiquement ajours les images et relancant les conteneurs dépendant avec la même command. 
La specification --restart permet à le relancé à chaque alumage du robot.
Vous pouvez alors librement choisir un interval de mise à jours des images docker sur nle robot.
Remarquans qu'on interval très rapide petis considérablement augement le network trafic.

Pour demarer le robot :
    ros2 launch turtlebot3_bringup robot.launch.py
Nous avons éssayer de meme automatiser cette command qui est la seule à devoir etre lancé à chaque fois.
Pour plus de détaille regarder le Readme de turtlebot_fichier_temp

### Network configuration
 
La configuration de réseaux et tous simple parle fichier :
/etc/netplan/50-cloud-init.yaml

```yaml
network:
    ethernets:
        eth0:
            dhcp4: true
            optional: true
    version: 2
    wifis:
        wlan0:
            dhcp4: yes
            dhcp6: yes
            access-points:
                "[Nom du Réseuax]":
                    password: "[mots de passe]"
```

##