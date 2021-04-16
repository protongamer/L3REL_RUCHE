
unsigned long x = 0;

unsigned long timer = 0;


void setup() {
  // put your setup code here, to run once:
Serial.begin(115200);


}

void loop() {
  // put your main code here, to run repeatedly:

if(millis() - timer >= 1000){
Serial.print("Coucou ");
Serial.println(x);
timer = millis(); //remise à 0
}


x++;

}
