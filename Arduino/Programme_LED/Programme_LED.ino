bool led; 

void setup() {
  // put your setup code here, to run once:

pinMode(13,OUTPUT);
pinMode(12,OUTPUT);
pinMode(8,INPUT_PULLUP);
}

void loop() {
  // put your main code here, to run repeatedly:

digitalWrite (12, 1); 
delay (1000); 
digitalWrite (12, 0); 
delay (1000);

led = digitalRead (8); 
digitalWrite (13, led);                                              

}
