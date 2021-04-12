

#include <EEPROM.h>

byte ChoixTempo = 0;


void setup() 

{

Serial.begin(9600);

EEPROM.write(10, 68);

for ( int i=0; i<=15;  i++ )
{
 
ChoixTempo = EEPROM.read (i); 
Serial.print (i); 
Serial.print ("\t"); 
Serial.println(ChoixTempo);

}



}

void loop() {
} 
