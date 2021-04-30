#include <SPI.h>
#include <RH_RF95.h>
#include <math.h>
#include <Wire.h>
#include "rgb_lcd.h"

#include <TimerOne.h>

#include <EEPROM.h>

#include "DHT.h"
#include "def.h"

rgb_lcd lcd;

// Singleton instance of the radio driver
RH_RF95 rf95(RFM95_CS, RFM95_INT);

int colorR = 255;
int colorG = 0;
int colorB = 0;

// Capteur température et humidité DHT22

#define DHTTYPE DHT22
DHT dht(DHTPIN, DHTTYPE);



int tab1 [4];
int tab2 [4] = {0, 0, 0, 0};

unsigned long temps = 0;
unsigned long temps_capteur;
unsigned long T_Blink = 0;
unsigned long temps_renvoi;
unsigned long LCD_veille;

int Ad_R = 1; // Adresse de la ruche
int Ad_S; // Adresse du serveur
int TempoStatut; // Temporisation statut (carte opérationnelle)
int TempoData = 1; // Temporisation activation des capteurs de la ruche
int nbre;// utiliser dans le mot de passe
int choix;// utiliser dans le mot de passe
int colonne_Curseur = 2 ;
uint16_t ChoixTempo = 1; // choix de la tempo dans les paramètres
uint16_t ChoixAdresse = 1; // choix de l'adresse de la ruche dans les paramètres

char Affichage = 0;
char Parametre = 0;
char Temperature = 0;
char Humidite = 0;
char c;

byte menu = 0;

float t; //température
float h; // humidité

bool BT1; // pouton poussoir de l'encodeur
bool flag = 0; // machine à état
bool flagEnc = 0; // machine à état pour encodeur
bool flagC = 0; // machine à état réception
bool etat = 0; // état du caractère
bool act = 0; // actionneur utiliser pour faire clignoter le caractère
bool Mdp = 0; // arbitre (vérifie si la condition est vrai ou fausse)


bool encoder_direct = 0;
bool encoder_rotate_flag = 0;

void affichage (int page); // Mode d'affichage (menu déroulant)
void ecriture(bool state) ; //Affichage du curseur
void blink_car(); // Clignotement d'un caractère
void trans (); // transmission
void recep(); // réception

////////////////////////////////////////////////////////////////////////////////
void setup()
{
  Serial.begin(115200);
  dht.begin();//phase initialisation capteur
  pinMode (BOUTON, INPUT); // bouton poussoir câclé sur la broche 6
  pinMode(LED, OUTPUT);
  pinMode(RFM95_RST, OUTPUT);
  pinMode(ENC_PIN_SIGA,INPUT); // encodeur câblé sur la broche 3
  pinMode(ENC_PIN_SIGB,INPUT); // encodeur câblé sur la broche 4
  pinMode(relay_pin, OUTPUT); // relais câblé sur la broche 8
  attachInterrupt(digitalPinToInterrupt(ENC_PIN_SIGA), encodeur_interrupt, RISING); // créer une interruption (interruption du programme temporairement) pour lire l'encodeur 
  
   ///////////////////////////////////////////////////////////////////////////
   // initialisation Lora
   
  digitalWrite(RFM95_RST, HIGH);  
  digitalWrite(RFM95_RST, LOW);
  delay(10);
  digitalWrite(RFM95_RST, HIGH);
  delay(10);

  if (!rf95.init())// vérification de l'initialisation
  {
    Serial.println("LoRa radio init failed");
    while (1); // tant que 1: arrêt programme
  }
  Serial.println("LoRa radio init OK!");

  
  if (!rf95.setFrequency(RF95_FREQ))// vérification du paramétrage de la fréquence de transmission
  {
    Serial.println("setFrequency failed");
    while (1);
  }
  Serial.print("Set Freq to: "); Serial.println(RF95_FREQ);

  rf95.setTxPower(23, false); // puissance d'émission
  delay(500);

  ////////////////////////////////////////////////////////////////////////////
  //Défini le nombre de colonne et de ligne

  lcd.begin(16, 2);
  lcd.setRGB(colorR, colorG, colorB);

  ///////////////////////////////////////////////////////////////////////////
  //lecture de l'EEPROM

  ChoixTempo = EEPROM.read(Adr_ChoixTempo); // lecture sauvegarde du choix de la tempo dans les paramètres
  ChoixAdresse = EEPROM.read(Adr_ChoixAdresse); // lecture sauvegarde du choix de l'adresse de la ruche dans les paramètres
  Serial.println(ChoixTempo);
  delay(5000);

  if (ChoixTempo < 1 || ChoixTempo > 24 || ChoixAdresse < 1 || ChoixAdresse > 99)
  {
    menu = 5;
  }

  /////////////////////////////////////////////////////////////////////////////
  // affichage du menu

  affichage(menu);

}//fin void setup


///////////////////////////////////////////////////////////////////////////
// fonction interruption pour lire l'encodeur

void encodeur_interrupt()
{

encoder_direct = digitalRead(ENC_PIN_SIGB); //rotation gauche ou droite de l'encodeur
encoder_rotate_flag = 1;
  
}




/////////////////////////////////////////////////////////////////////////////
// Void loop

void loop()
{

if(encoder_rotate_flag == 1){
  Serial.println(encoder_direct);
}

  if (Serial.available () > 0)
  {
    c = Serial.read();
  }
  BT1 = digitalRead (BOUTON);

  /////////////////////////////////////////////////////////////////////////
  // Utilisation d'un relais pour activer le capteur température/humidité


  if (millis() - temps_capteur >= ((unsigned long)ChoixTempo * 1000) * 60) // temporisation activation du capteur toutes les heures
  {
    digitalWrite(relay_pin, HIGH);
    delay(3000);

    dht.begin();
    h = dht.readHumidity();// humidité
    t = dht.readTemperature();// température
    Serial.print (t);
    Serial.print ("\t");
    Serial.println (h);

    delay (5000);

    
    byte compteurLocal = 0;
    while (flagC == 0)
    {
      if (millis() - temps_renvoi >= TIMEOUT_RX)
      {
        trans(); 

        compteurLocal++;
        temps_renvoi = millis();
      }
      
      if (compteurLocal > 5) {
        flagC = 1;
      }
      
      recep();
    }
    
    compteurLocal = 0;
    flagC = 0;
    digitalWrite (relay_pin, LOW);
    temps_capteur = millis();

  }
/////////////////////////////////////////////////////////////////////
// activation de l'écran LCD et mis en veille de l'écran LCD 

if (encoder_rotate_flag == 1 || BT1 == 1)
  {
   LCD_veille = millis(); 
   colorR = 255;
   lcd.setRGB(colorR, colorG, colorB);
  }

if (millis () - LCD_veille >= TIME_LCD)
  {
  colorR = 0;
  lcd.setRGB(colorR, colorG, colorB);
  } 

///////////////////////////////////////////////////////////////////////
// temporisateur pour lire la température et l'humidité

if ( millis () - temps >= 1000 && (menu == 3 || menu == 2) )
{
  temps = millis(); //remise à 0
  affichage (menu);
}

///////////////////////////////////////////////////////////////////////
// Navigation d'un menu à l'autre

if (BT1 == 0 && flag == 1)
{
  affichage(menu);
  flag = 0;
}

if (BT1 == 1 && flag == 0 && menu == 0)
{
  if (encoder_direct == ENC_HAUT)
  {
    menu = 1;
  }
  else
  {
    menu = 4;
    lcd.setCursor (0, 1);
    lcd.print ("                   ");
  }
  flag = 1;
}

else if (BT1 == 1 && flag == 0 && menu == 1)
{
  if (encoder_direct == ENC_HAUT)
  {
    menu = 2;
  }
  else
  {
    menu = 3;
  }
  flag = 1;
}

else if (BT1 == 1 && flag == 0 && menu == 2)
{
  menu = 0;
  flag = 1;
}

else if (BT1 == 1 && flag == 0 && menu == 3)
{
  menu = 0;
  flag = 1;
}

else if ( menu == 4)
{
  blink_car() ;
}



///////////////////////////////////////////////////////////////
// Position de l'encodeur (sauf menu 4,5 et 6)


if ( menu != 4 && menu != 5 && menu != 6)
{

  if (encoder_direct == 1 && flagEnc == 0)

  {
    ecriture(ENC_BAS);
    flagEnc = 1;
  }
  else if (encoder_direct == 0 && flagEnc == 1)
  {
    ecriture(ENC_HAUT);
    flagEnc = 0;
  }

  encoder_rotate_flag = 0;
}

//////////////////////////////////////////////////////////////
///Position encodeur pour le menu 4: mot de passe

if (encoder_rotate_flag == 1 && menu == 4 && act == 1)
{
  lcd.setCursor(colonne_Curseur, 1);
  lcd.print (nbre);

  if (encoder_direct == 1)
  {
    nbre++;
    if (nbre > 9)
      nbre = 9;
  }
  else
  {
    nbre--;
    if (nbre < 0)
      nbre = 0;
  }
  encoder_rotate_flag = 0;

}

if (BT1 == 1 && flag == 0 && menu == 4)
{
  choix = nbre;
  lcd.setCursor (colonne_Curseur, 1);
  lcd.print (choix);
  tab1[colonne_Curseur - 2] = choix;
  if (colonne_Curseur <= 5)
  {
    colonne_Curseur++;
  }
  flag = 1;
}

//////////////////////////////////////////////////////////////
/// vérification du mot de passe

if (colonne_Curseur > 5)
{
  Mdp = 1; //valeur initiale // ne change si aucun chiffre de tab1 est différent de tab2

  for (int i = 0; i < 4; i++)
  {
    if (tab1[i] != tab2[i])
    {
      Mdp = 0;
    }
  }
  if (Mdp == 1)
  {
    lcd.setCursor(0, 1);
    lcd.print (" Acces autorise");
    delay (5000);
    menu = 5;
  }
  else
  {
    lcd.setCursor(0, 1);
    lcd.print (" Acces refuse  ");
    delay (5000);
    menu = 0;
  }

  colonne_Curseur = 2 ;
}

////////////////////////////////////////////////////////////////////
//menu 5: choix de la tempo dans les paramètres (TempoData)

if ( menu == 5 ) {

  if (encoder_rotate_flag == 1 )
  {

    if (encoder_direct == 1)
    {
      TempoData++;
      if (TempoData > 24)
        TempoData = 24;
    }
    else
    {
      TempoData--;
      if (TempoData < 1)
        TempoData = 1;
    }
    encoder_rotate_flag = 0;

    lcd.setCursor(1, 1);
    lcd.print("    ");
    lcd.setCursor(1, 1);
    lcd.print (TempoData);
    lcd.print("h");
  }

  if (BT1 == 1 && flag == 0)
  {
    ChoixTempo = TempoData;
    EEPROM.write (Adr_ChoixTempo, ChoixTempo);
    lcd.setCursor (1, 1);
    lcd.print (ChoixTempo);
    delay (5000);
    menu = 6;
    flag = 1;
  }

}//menu = 5

////////////////////////////////////////////////////////////////
//menu 6: Choix de l'adresse de la ruche dans les paramètres (Ad_R)

if ( menu == 6) {

  if (encoder_rotate_flag == 1 )
  {
    if (encoder_direct == 1)
    {
      Ad_R++;
      if (Ad_R > 99)
        Ad_R = 99;
    }
    else
    {
      Ad_R--;
      if (Ad_R < 1)
        Ad_R = 1;
    }
    encoder_rotate_flag = 0;

    lcd.setCursor(1, 1);
    lcd.print("    ");
    lcd.setCursor(1, 1);
    lcd.print (Ad_R);
  }

  if (BT1 == 1 && flag == 0)
  {
    ChoixAdresse = Ad_R;
    EEPROM.write (Adr_ChoixAdresse, ChoixAdresse);
    lcd.setCursor (1, 1);
    lcd.print (ChoixAdresse);
    delay (5000);
    menu = 0;
    flag = 1;
  }

}//menu = 6


} //fin void loop


//////////////////////////////////////////////////////////////
//Fonctions


void affichage (int page)
{
  if (page == 0)
  {
    lcd.setCursor(0, 0);
    lcd.print (" Affichage     ");
    lcd.setCursor(0, 1);
    lcd.print (" Parametres    ");
  }
  else if (page == 1)
  {
    lcd.setCursor(0, 0);
    lcd.print (" Temperature");
    lcd.setCursor(0, 1);
    lcd.print (" Humidite  ");
  }
  else if (page == 2)
  {
    lcd.setCursor(0, 0);
    lcd.print (" Ruche:      ");
    lcd.print (Ad_R);
    lcd.setCursor(0, 1);
    lcd.print (" T: ");
    lcd.print (t);
    lcd.print (" ");
    lcd.write(DEG_CHR);
    lcd.print ("C");
  }
  else if (page == 3)
  {
    lcd.setCursor(0, 0);
    lcd.print (" Ruche:     ");
    lcd.print (Ad_R);
    lcd.setCursor(0, 1);
    lcd.print (" H:  ");
    lcd.print (h);
    lcd.print (" %");
  }
  else if (page == 4)
  {
    lcd.setCursor(0, 0);
    lcd.print (" Mot de passe        ");
  }
  else if (page == 5)
  {
    lcd.setCursor (0, 0);
    lcd.print (" Temporisation      ");
    lcd.setCursor (1, 1);
    lcd.print ("                    ");
    lcd.setCursor (1, 1);
    lcd.print (ChoixTempo);
    lcd.print("h");

  }
  else if (page == 6)
  {
    lcd.setCursor (0, 0);
    lcd.print (" Adresse ruche      ");
    lcd.setCursor (1, 1);
    lcd.print ("                    ");
    lcd.setCursor (1, 1);
    lcd.print (ChoixAdresse);
  }
}





//////////////////////////////////////////////////////////////////////
//  Affichage du curseur

void ecriture(bool state)
{
  {
    if (state == ENC_HAUT)
    {
      lcd.setCursor(0, 0);
      lcd.print ("*");
      lcd.setCursor(0, 1);
      lcd.print (" ");
    }
    else if (state == ENC_BAS)
    {
      lcd.setCursor(0, 0);
      lcd.print (" ");
      lcd.setCursor(0, 1);
      lcd.print ("*");
    }
  }

}

///////////////////////////////////////////////////////////////////////////////
// clignotement d'un caractère

void blink_car()
{

  if ( BT1 == 1 )
  {
    act = 1;
  }
  if ( act == 1 && millis () - T_Blink >= 1000 )
  {
    Serial.print (etat);
    lcd.setCursor(colonne_Curseur, 1 );
    if (etat)
    {
      lcd.write (CURSEUR);
    }
    else
    {
      lcd.print (nbre);
    }

    etat = !etat;

    T_Blink = millis(); //remise à 0
  }
}
//////////////////////////////////////////////////////////////////////////////////////
// Transmission

void trans ()
{
  
  // calcul et envoie tram
  float temp = t;
  float hum = h;


  uint8_t data[6];
  data[0] = 0; // adresse
  data[1] = ChoixAdresse;
  data[2] = int(temp); //partie entière temperature
  data[3] = int((temp - int(temp)) * 100); //partie décimale temperature
  data[4] = int(hum); //partie entière humidité
  data[5] = int((hum - int(hum)) * 100); //partie décimale humidité

  for (int i = 0; i < 5; i++) {
    Serial.print(data[i]);
    Serial.print("\t");
  }
  Serial.println();


  rf95.send(data, sizeof(data)); // envoie
  rf95.waitPacketSent(); // tempo vérification de l'envoi
  Serial.println("Sent a reply"); // message "bien envoyé"
  digitalWrite(LED, LOW);

}
///////////////////////////////////////////////////////////////////////////////////
// Réception

void recep()
{
  if (rf95.available())
  {
    uint8_t buf[RH_RF95_MAX_MESSAGE_LEN]; // création d'un tableau pour la tram
    uint8_t len = sizeof(buf); // longueur du tableau 

    if (rf95.recv(buf, &len))
    {
      digitalWrite(LED, HIGH);
      RH_RF95::printBuffer("Received: ", buf, len);
      Serial.print("Got: ");
      Serial.println((char*)buf);
      Serial.println(buf[0]);

      if (buf[0] == 'p') 
      {
        flagC = 1;
      }
    }
    else
    {
      Serial.println("Receive failed");
    }
  }
}
