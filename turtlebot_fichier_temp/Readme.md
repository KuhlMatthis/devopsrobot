# Fichier pour le robot:

ici sont les fichiers robot:

Le fichier-rc.local pour l'incrementation du espace user au premier chargement génerer par script lors de la réduction de la taille de l'image très intérrésant.
Le fichier rc.local pour lancé le docker et le bringup ros mais attention sans erreurs dans journalctl cellui semble pour autont pas encore fonctioner correctement.
Les fichiers  ros pour dépendance éxécution hardware.sh et systemdservice pour lancé un service du projet:
Le fichier createimage pour list d'utile pour creer des images raspberry pi
Command line: 
```
sudo systemctl enable tempMonitor.service
sudo service tempMonitor status/start/stop
```

