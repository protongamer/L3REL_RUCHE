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


// Variable menu Paramètres
int Ad_R; // Adresse de la ruche
int Ad_S; // Adresse du serveur
int TempoStatut; // Temporisation statut (carte opérationnelle)
int TempoData; // Temporisation activation des capteurs de la ruche

char Affichage = 0;
char Parametre = 0;
char Temperature = 0;
char Humidite = 0;
char c;

byte menu = 0;

int h;
float t;

bool BT1; // pouton poussoir de l'encodeur
bool flag = 0; // machine à état
bool flagEnc = 0; // machine à état pour encodeur



void setup()
{
  Serial.begin(115200);
  dht.begin();//phase initialisation capteur
  pinMode (4, INPUT); // bouton poussoir câclé sur la broche 4
  encoder.Timer_init();

  // Défini le nombre de colonne et de ligne
  lcd.begin(16, 2);
  lcd.setRGB(colorR, colorG, colorB);
  
  affichage(menu);
}


void loop()
{
  
  if (Serial.available () > 0)
  {
    c = Serial.read();
  }

  BT1 = digitalRead (4);


  h = dht.readHumidity();// humidité
  t = dht.readTemperature();// température
  Serial.print(h);
  Serial.print("\t");
  Serial.println(t);


  if (BT1 == 0 && flag == 1)
  {
    affichage(menu);
    flag = 0;
  }

  if (BT1 == 1 && flag == 0 && menu == 0)
  {
    if (encoder.direct == ENC_HAUT) {
      menu = 1;
    } else {
      //menu = 3;
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
    flag = 1;
  }

  else if (BT1 == 1 && flag == 0 && menu == 3)
  {
    flag = 1;
  }



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








/////////////////////////////////////////////////////
//Fonctions


void affichage (int page)
{

  if (page == 0)
  {
    lcd.setCursor(0, 0);
    lcd.print (" Affichage");
    lcd.setCursor(0, 1);
    lcd.print (" Parametres");
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
    lcd.print (" Ruche:      ");
    lcd.print (Ad_R);
    lcd.setCursor(0, 1);
    lcd.print (" H: ");
    lcd.print (h);
    lcd.print (" %");
  }


}






void ecriture(bool state) 
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
