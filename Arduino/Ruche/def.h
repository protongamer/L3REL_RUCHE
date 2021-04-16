#define ENC_HAUT    0
#define ENC_BAS     1


//////////////////////////
//BROCHES

#define LED        13 //led
#define BOUTON     6 //bouton
#define DHTPIN     5 //capteur

/////////////////////////
//encodeur
#define ENC_PIN_SIGA  3 // interruption intégrer pour "activer l'encodeur" 
#define ENC_PIN_SIGB  4 // permet la rotation gauche/droite

#define TIMEOUT_RX  5000 // temporisateur réception/transmission
#define TIME_LCD    10000 // temporisateur mise en veille écran LCD

#define DEG_CHR     223
#define CURSEUR     255
#define Adr_ChoixTempo 0 // adresse du choix de la tempo pour l'activation des capteurs
#define Adr_ChoixAdresse 1 // adresse du choix de l'adresse de la ruche 





///////////////////////////////
//LORA DEFs
#define RFM95_CS 10
#define RFM95_RST 9
#define RFM95_INT 2

#define RF95_FREQ 868.0
