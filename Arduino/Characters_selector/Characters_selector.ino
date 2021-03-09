#include <Wire.h>
#include "rgb_lcd.h"
#include <TimerOne.h>

char c;
byte k;

rgb_lcd lcd;


void setup() {
  
Serial.begin(115200);
lcd.begin(16, 2);
lcd.setRGB(0, 255, 0);


}

void loop() {

if(Serial.available() > 0){
c = Serial.read();  
Serial.println(k);

lcd.setCursor(0,0);
for(int i = k; i < k+16; i++){
lcd.write(i);
}
lcd.setCursor(0,1);
for(int i = k+16; i < k+32; i++){
lcd.write(i);  
}

}


switch(c){
  
  case '+':
  k+=32;
  break;

  case '-':
  k-=32;
  break;
  
}


c = 0;

}
