# L3REL_RUCHE


__Rapport 15/02/2021__

Test du matériel à disposition


à regarder de près finalement:

https://www.lextronic.fr/shield-arm-n8-lorawan-pour-raspberry-17349.html

~~Voir le contrôle des modules par commandes AT (15/02/2021 21:27)



__Rapport 16/02/2021__

Les modules LORA sont des modules LoRA comprenant une interface capable d'utiliser l'UART(donc il n'y aura suremment aucun soucis de compatibilité avec la Raspberry PI 3, comme nous avions discuté en présentiel) et de le paramétrer à l'aide d'un setup en utilisant les commandes AT par voie série et OTA. (Voir datasheet p.18)
Cepedant il faut envoyer la commande pour entrer dans le menu(soit '+++' → datasheet p.14 p.18)

La fréquence du port série du module pour communiquer est de ***19200 bauds***  (valeur par défaut ? Aucune info concernant ceci)

Il également spécifié que ce module à un mode bridge qui serait intéressant d'exploiter (p.13 p.19), ainsi que le mode low power(intéressant si on travaille sur batterie dont on peut relever le niveau apparemment à l'aide du test mode p.23)


Prochaine étape à réaliser :

Paramétrer les modules en fonction des commandes AT(p.18 ~ p.20), et vérifier si la communication se réalise correctent entre 2 modules.
