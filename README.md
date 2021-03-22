# L3REL_RUCHE


__Rapport 15/02/2021__

Test du matériel à disposition


à regarder de près finalement:

https://www.lextronic.fr/shield-arm-n8-lorawan-pour-raspberry-17349.html

~~Voir le contrôle des modules par commandes AT (15/02/2021 21:27)~~



__Rapport 16/02/2021__

Les modules LORA sont des modules LoRA comprenant une interface capable d'utiliser l'UART(donc il n'y aura suremment aucun soucis de compatibilité avec la Raspberry PI 3, comme nous avions discuté en présentiel) et de le paramétrer à l'aide d'un setup en utilisant les commandes AT par voie série et OTA. (Voir datasheet p.18)
Cepedant il faut envoyer la commande pour entrer dans le menu(soit '+++' → datasheet p.14 p.18)

La fréquence du port série du module pour communiquer est de ***19200 bauds***  (valeur par défaut ? Aucune info concernant ceci)

Il également spécifié que ce module à un mode bridge qui serait intéressant d'exploiter (p.13 p.19), ainsi que le mode low power(intéressant si on travaille sur batterie dont on peut relever le niveau apparemment à l'aide du test mode p.23)


Prochaine étape à réaliser :

Paramétrer les modules en fonction des commandes AT(p.18 ~ p.20), et vérifier si la communication se réalise correctent entre 2 modules.


__Rapport 22/02/2021__


Le module est un ARM-N8-LW et non un ARM-N8-LWR !

Ceci dit, il implémente des commandes compatibles avec le ARM-N8-LWR


~~à voir si ilest possible d'en tirer quelque chose(car le module est obsolète, difficile de trouver une doc à jour !)~~

https://yadom.fr/media/product-attachment//home/magento///File-1574072753.pdf


EDIT (18:54) : Problème avec les modules ARM-N8-LW ! Les commandes AT (ATM et ATO) répondent correctement, l'écriture du buffer de la RAM à l'EEPROM pour les registres ATM et ATO se fait correctement également, mais l'envoi des trames via la modulation de fréquence ne se fait pas. Donc aucune communication n'est donc possible via le RF Bridge(voir Mode Normal de la datasheet p.21 du lien juste au dessus). J'ai essayé donc toute les transmission possibles pour les 2 Modules, soit la transmission LoRa ou FSK en local, soit en LoRaWan via le réseau(sachant qu'il faut passer par un gateway, ce qui ne serait pas intéressant du au temps de transmission). De plus l'utiliser sur Sigfox n'est pas intéressant, il faut apparemment un abonnement pour pouvoir transmettre. Il serait préférable d'utiliser un autre module LoRa, à regarder de près pour la compatibilité Arduino/RPI : https://www.adafruit.com/product/3072



__Rapport 23/02/2021__


Premier tests de la RPI 3 :

-RPI 3 ok
-Ecran 3.5" GPIO ok


Intégration d'un code test Python pour l'affichage de l'IHM

Lien pour l'encodeur grove: https://www.lextronic.fr/module-grove-encodeur-rotatif-17275.html


__Rapport 06/03/2021__

Update du script python:

-Séquence boot
-Peut lire des fichier textes(intéressant pour lire la base de donnée)
-Affiche la date et l'heure en temps réel
-Affiche la température et l'humidité en fonction de la ruche correspondante


EDIT : Intégration du parseur → fait


![alt_text](https://github.com/protongamer/L3REL_RUCHE/blob/main/pictures/demo.png?raw=true)



__Rapport 07/03/2021__


Réalisation de l'analyse fonctionnelle

![alt_text](https://github.com/protongamer/L3REL_RUCHE/blob/main/pictures/Diagramme_Ruche.png?raw=true)


Réalisation du cahier des charges


__Rapport 09/03/2021__

Solution pour la page web: p5.js

→ établir un serveur local

https://github.com/processing/p5.js/wiki/Local-server




__Rapport 14/03/2021__

Intégration de la page web fait !

![alt_text](https://github.com/protongamer/L3REL_RUCHE/blob/main/pictures/screen_openiob.png?raw=true)

idée d'utilisation pour mettre en place un serveur simple, en utilisant la commande sous Raspberry Pi OS (Anciennement Raspbian):

``` python3 -m http.server --directory /chemin/du/dossier```



__Rapport 22/03/2021__


-Réalisation d'une demande de code PIN local sur LCD pour accéder au paramètres de la Ruche en local.
(Photo ici)

-Test de liaison des modules LoRa (base RFM95 / chip SX1276) : ok
Réalisé entre 2 Arduino s'envoyant chacun leur tour un message (1 depuis une station de travail, et 1 portatif)
(photo calculette)

Ci-joint le log du 22032021.txt des résultat de la trame avec quelques erreurs de réception (à suivre de près), durant l'expérience menée sur une trajectoire de 200m à vol d'oiseau en champs avec des obstacles.

(photo google maps)

