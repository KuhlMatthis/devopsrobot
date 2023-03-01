# Devops dans la robotique


## Partie turtlebot:

###  Utilisation de l'Image

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
```BASH
ros2 launch turtlebot3_bringup robot.launch.py
```
Nous avons éssayer de meme automatiser cette command qui est la seule à devoir etre lancé à chaque fois.
Pour plus de détaille regarder le Readme de turtlebot_fichier_temp

### Network configuration
 
La configuration de réseaux est configurer par le fichier:

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

## Project workflow

### Developement du projet est test local ou sur le robot

Pour tester votre projet vous pouvez placer ou modifier le docier src dans ros_master_foxy/ros2_basics/cpp_topic ceci est votre projet ros.
Il n'est pas nécésaire de builder le projet le fichier docker son ocupe.

Pour lancé le projet ros depuis le dosier ros_master_foxy: 
Vous pouvez builder le projet avec:
```
sudo docker build --build-arg base="ros:foxy" -t turtlebotfoxy . 
```
puis le lancer:
```
sudo docker run -it turtlebotfoxy
```
Après rien ne vous oblige de l'utiliser.
Dans ce repartopir vous avez aussi un script de lancement:
simulationtest.sh qui lance automatiquement  turtlebot3_gazebo et le contenaire docker.

Lorsque votre robot est directement connecter à votre réseaux vue que foxy utlise Du ddsfastest(multicast) vous pourez directement le tester aussi sur le robot.
La variable ROS_HOSTNAME sur le robot et dans le docker est de base à 30 mais vous pouvez le modifier.
Pour le robot dans le fichier ~/.bashrc.
pour verifier la varible ```echo $ROS_HOSTNAME```
Et dans le docker dans le dockerfile ligne 16: ENV ROS_DOMAIN_ID=30


Il existe deux branch dans ce projet le main qui pour la publication
et le test qui est la vérification. Lorsque un code est push sur l'un de c'est deux topic les action github ce trouvans dans le dosier
.github\workflows sont executer.
github-action-build.yml pour le push sur le main.
et github-actions-test.yml pour un push sur la branch test.

Si nous regardons c'est gihtub actions de plus près:

### github-action-test branch test

Lorsque vous pushez sur test vous pouvez observer le bilan de Trivy CVES image analyse de l'image docker de votre projet.
Celle si sont visible si aucun risque High ou Critical. Dans le github du projet sous action séléctioner l'action avec le #numero corréspondant à votre push (souvant le dernier).
Puis dans 'Test docker image' et l'angle: 'Get Trivy CVES image analyse with securtiy vulnerability for the image' vous avez tous le bilan.
Si il existe des problème de sécurité reporter HIGH or CRITICAL il est fortment déconseille de push le code sur la branche main !

### github-action-build branch main
Une des actions est de s'inscrir dans docker hub afin de pouvoir push des image dessus
```
 - name: Login to Docker Hub
        uses: docker/login-action@v2
        with:
          username: ${{ secrets.DOCKERHUB_USERNAME }}
          password: ${{ secrets.DOCKERHUB_TOKEN }}
```
Il vous serraz nécésaire de creer ces deux secrets sur ce projet dans github
sous l'angle Settings puis Secrets/variables/actions puis clicker sur a Nex repository secret.

par la suite le projet est push sur github à la ligne 49 vous trouvez les tags ou celle si sont push

```
    tags: ${{secrets.DOCKERHUB_USERNAME}}/test:latest, ${{secrets.DOCKERHUB_USERNAME}}/test:${{github.run_number}}
```

Si vous modifier c'est tag il serra nécésaire de mettre à jours le push du projet dans le robot pour cella sur le robot:
```BASH
docker pull  [secrets.DOCKERHUB_USERNAME]/[tag name (test)]:latest
```
pour le lancement qu'une ligne à change dans /etc/rc.local (après le first boot de l'image sur la Rapsberry Pi si non rc.local.bak)

```
docker run --rm --name control [secrets.DOCKERHUB_USERNAME]/[tag name (test)]:latest > /home/ubuntu/output.txt 2>&1 &
```


## Conclusion

Conclusion votre projet robotique en mode devops pour du turtlebot est près.
Si vous etes intéréssé à construire un projet ressemblant sur un autre robot ou systeme vous pouvez regarder de plus proche les détaille de créaation image et les fichier turtlebot_temporaire.
Pour améliorer ce projet il est intérésant de rajouter des test automatique dans le github action branche test et surtous à réussir le lancement ros2 hardwaire sur la Raspberry Pi de maniere automatique. Nous avons ouvert un issue à ce sujet et sont prénon de toute participation.