#include "DHT.h"
#include <math.h>
#include <Wire.h>
#include "rgb_lcd.h"
#include <Encoder.h>
#include <TimerOne.h>
#include "def.h"



rgb_lcd lcd;

const int colorR = 255;
const int colorG = 0;
const int colorB = 0;

// Capteur température et humidité DHT11
#define DHTPIN 5
#define DHTTYPE DHT11
DHT dht(DHTPIN, DHTTYPE);

int relay_pin = 8;

int tab1 [4];
int tab2 [4] = {0, 0, 0, 0};

unsigned long temps = 0;
unsigned long temps_capteur;
unsigned long T_Blink = 0;

int Ad_R; // Adresse de la ruche
int Ad_S; // Adresse du serveur
int TempoStatut; // Temporisation statut (carte opérationnelle)
int TempoData; // Temporisation activation des capteurs de la ruche
int h;
int nbre;
int choix;
int colonne_Curseur = 2 ;
uint16_t ChoixTempo = 1;

char Affichage = 0;
char Parametre = 0;
char Temperature = 0;
char Humidite = 0;
char c;

byte menu = 0;

float t;

bool BT1; // pouton poussoir de l'encodeur
bool flag = 0; // machine à état
bool flagEnc = 0; // machine à état pour encodeur
bool etat = 0; // état du caractère
bool act = 0; // actionneur utiliser pour faire clignoter le caractère
bool Mdp = 0; // arbitre (vérifie si la condition est vrai ou fausse)


void affichage (int page);
void ecriture(bool state) ;
void blink_car();

////////////////////////////////////////////////////////////////////////////////
void setup()
{
  Serial.begin(115200);
  dht.begin();//phase initialisation capteur
  pinMode (4, INPUT); // bouton poussoir câclé sur la broche 4
  encoder.Timer_init();
  pinMode(relay_pin, OUTPUT); // relais câblé sur la broche 8

  // Défini le nombre de colonne et de ligne
  lcd.begin(16, 2);
  lcd.setRGB(colorR, colorG, colorB);

  affichage(menu);
}

/////////////////////////////////////////////////////////////////////////////
// Void loop

void loop()
{

  if (Serial.available () > 0)
  {
    c = Serial.read();
  }
  BT1 = digitalRead (4);

  /////////////////////////////////////////////////////////////////////////
  // Utilisation d'un relais pour activer le capteur

Serial.print(((unsigned long)ChoixTempo*1000)*3600);
Serial.print("\t");
Serial.println(millis() - temps_capteur);

  if (millis() - temps_capteur >= ((unsigned long)ChoixTempo*1000)*3600) // temporisation activation du capteur toutes les heures 
{
  digitalWrite(relay_pin, HIGH);
  delay(3000);

  //if (carte prête)
  
  dht.begin();
  h = dht.readHumidity();// humidité
  t = dht.readTemperature();// température
  Serial.print (t);
  Serial.print ("\t"); 
  Serial.println (h); 
    
  delay (5000);

  // if (retour ok)
  
  digitalWrite (relay_pin, LOW);

temps_capteur = millis();

}


  ///////////////////////////////////////////////////////////////////////
  // temporisateur pour le capteur température/humidité

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
  if (encoder.direct == ENC_HAUT)
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
  if (encoder.direct == ENC_HAUT)
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
  // Position de l'encodeur


  if ( menu != 4 && menu != 5)
{

  if (encoder.direct == 1 && flagEnc == 0)

    {
      ecriture(ENC_BAS);
      flagEnc = 1;
    }
    else if (encoder.direct == 0 && flagEnc == 1)
    {
      ecriture(ENC_HAUT);
      flagEnc = 0;
    }

    encoder.rotate_flag = 0;
  }

  //////////////////////////////////////////////////////////////
  ///Position encodeur pour le menu 4

  if (encoder.rotate_flag == 1 && menu == 4 && act == 1)
{
  lcd.setCursor(colonne_Curseur, 1);
    lcd.print (nbre);

    if (encoder.direct == 1)
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
    encoder.rotate_flag = 0;

}

  if (BT1 == 1 && flag == 0 && menu==4)
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
  // TempoData

if( menu == 5 ){

  if (encoder.rotate_flag == 1 )
{
  lcd.setCursor(1, 1);
  lcd.print("    ");
  lcd.setCursor(1, 1);
  lcd.print (TempoData);
  lcd.print(" h");
    if (encoder.direct == 1)
    {
      TempoData++;
      if (TempoData > 56)
        TempoData = 56;
    }
    else
    {
      TempoData--;
      if (TempoData < 0)
        TempoData = 0;
    }
    encoder.rotate_flag = 0;


    
}

  if (BT1 == 1 && flag == 0)
  {
  ChoixTempo = TempoData;
  lcd.setCursor (1, 1); 
  lcd.print (ChoixTempo);

   
  }

}//menu = 5




   
}


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
