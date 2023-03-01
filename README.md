# Devops dans la robotique


## Partie turtlebot:

###  Utilisation de l'image

Vous pouvez récupérer l'image pour la Raspberry Pi du turtlebot utilisée dans notre projet
à l'adresse suivante :  https://drive.google.com/file/d/131MRJGBEvVxsQqDuKMeZVtstDKENaFzl/view.
Cette image a l'avantage d'être exactement dans l'état actuel de notre projet.
Cette image sera, avec votre outil préféré, chargée sur la carte ssd de la Raspberry Pi:
Dans notre projet nous avons utilisé Pi Imager qui est l'outil le plus récent et très simple d'utilisation.
Il suffit de sélectionner directement le fichier zip de l'image téléchargée puis sélectionner la carte et cliquer sur write.
Les options spécifiques sur cette image ne vous seront actuellement d'aucune utilité puisqu'ils ne sont pas implémentés sur l'image de base de turtlebot.

Lorsque l'image est chargée sur la carte ssd vous pouvez lancer le robot.
Avec docker ps vous devriez aperçevoir un conteneur docker tourner, c'est le conteneur ros du projet créé.

La toute première fois pour la mise à jour automatique des conteneurs vous pouvez utiliser watchtower avec par exemple cette commande:
```BASH
docker run -d \
    --name watchtower \
    --restart unless-stopped \
    -v /var/run/docker.sock:/var/run/docker.sock \
    containrrr/watchtower -c \
    --interval 3600
```

Watchtower est un conteneur permettant de mettre automatiquement à jour les images et relançant les conteneurs dépendant de cette image avec la même commande que celle avec laquelle ils ont été lancés la première fois. 
La spécification --restart permet à le relancer à chaque allumage du robot.
Vous pouvez alors librement choisir un --interval de mise à jour des images docker sur le robot.
Remarquons qu'un intervalle très rapide donc petit augmente considérablement le network trafic.

Pour démarrer le robot :
```BASH
ros2 launch turtlebot3_bringup robot.launch.py
```
Nous avons aussi essayé d'automatiser cette commande qui est la seule à devoir être lancée à chaque fois.
Pour plus de détails voir le Readme de turtlebot_fichier_temp

### Configuration du Network
 
Le réseau est configuré par le fichier :
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

### Développement du projet et test local ou sur le robot

Pour tester votre projet vous pouvez placer ou modifier le dossier src dans ros_master_foxy/ros2_basics/cpp_topic ceci est votre projet ros.
Il n'est pas nécessaire de builder le projet, le fichier docker s'en occupe.

Pour lancer le projet ros depuis le dossier ros_master_foxy: 
Vous pouvez builder l'image docker avec:
```
sudo docker build --build-arg base="ros:foxy" -t turtlebotfoxy . 
```
puis lancer un conteneur de cette image:
```
sudo docker run -it turtlebotfoxy
```
Ceci étant rien ne vous oblige à vous en servir.
Dans ce répertoire vous avez aussi un script de lancement:
simulationtest.sh qui lance automatiquement turtlebot3_gazebo et le conteneur docker.

Lorsque votre robot est directement connecté à votre réseau vous pouvez directement le tester aussi sur le robot vu que foxy utilise du ddsfastest(multicast).
La variable ROS_HOSTNAME sur le robot et dans le docker est de base à 30 mais vous pouvez la modifier.
Pour le robot dans le fichier ~/.bashrc.
Pour vérifier la variable ```echo $ROS_HOSTNAME```
Et dans le docker pour modifier cette variable il suffit de modifier la ligne 16 dans le dockerfile: ENV ROS_DOMAIN_ID=30

### Github action

Il existe deux branches dans ce projet la branche main qui est pour la publication et la branche test qui est pour tester le projet. Lorsqu'un code est push sur l'une de ces deux branches les actions github se trouvant dans le dossier .github\workflows sont éxecutées.
Les actions de github-action-build.yml pour le push sur le main et
celles de github-actions-test.yml pour un push sur la branche test sont éxecutées.

#### github-action-test branch test

Lorsque vous pushez sur test vous pouvez observer le bilan de Trivy CVES image analyse de l'image docker de votre projet.
Ce bilan est visible dans le github du projet dans l'onglet action où il faut sélectionner l'action avec le #numero correspondant à votre push (souvent le dernier),
puis dans 'Test docker image' et l'onglet: 'Get Trivy CVES image analyse with securtiy vulnerability for the image'.
S'il existe des problèmes de sécurité rapportés HIGH or CRITICAL il est fortement déconseillé de push le code sur la branche main !

#### github-action-build branch main

Une des actions dans le main est de s'inscrire dans docker hub afin de pouvoir push des images dessus
```yaml
 - name: Login to Docker Hub
        uses: docker/login-action@v2
        with:
          username: ${{ secrets.DOCKERHUB_USERNAME }}
          password: ${{ secrets.DOCKERHUB_TOKEN }}
```
Il vous sera nécessaire de créer ces deux secrets sur ce projet dans github
sous l'onglet Settings puis Secrets/variables/actions puis cliquer sur a New repository secret.

Par la suite le projet est push sur github.
A la ligne 49 vous trouvez les tags sous lesquels cette image est push.

```yaml
    tags: ${{secrets.DOCKERHUB_USERNAME}}/test:latest, ${{secrets.DOCKERHUB_USERNAME}}/test:${{github.run_number}}
```

Si ces tags sont modifiés il sera nécessaire de mettre à jour le push du projet dans le robot. Pour cela vous pouvez lancer la commande suivante sur le robot :
```BASH
docker pull  [secrets.DOCKERHUB_USERNAME]/[tag name (test)]:latest
```
Ensuite pour le lancement du conteneur docker qu'une ligne a changé dans /etc/rc.local (après le first boot de l'image sur la Rapsberry Pi sinon rc.local.bak)
```
docker run --rm --name control [secrets.DOCKERHUB_USERNAME]/[tag name (test)]:latest > /home/ubuntu/output.txt 2>&1 &
```
Penser à supprimer les images et conteneurs inutiles pour votre projet puisqu'ils risquent de prendre beaucoup de place.
```
docker images -a
docker container ls
docker container rm [container name]
docker image rm [image name]
```




## Conclusion

Votre projet robotique en mode devops pour du turtlebot est prêt.
Si vous êtes intéressés à construire un projet ressemblant sur un autre robot ou système vous pouvez regarder de plus près les détails de création image et les fichiers turtlebot_temporaire.
Pour améliorer ce projet il est intéressant de rajouter des tests automatiques dans le github action branche test et surtout de réussir le lancement ros2 hardwaire sur la Raspberry Pi de manière automatique. Nous avons ouvert une issue à ce sujet et sommes preneurs de toute participation.