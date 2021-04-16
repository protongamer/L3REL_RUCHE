
    int relay_pin = 8;
    int led_pin = 13;
    
    void setup(){ 
      pinMode(relay_pin,OUTPUT);
      pinMode(led_pin,OUTPUT);  
    digitalWrite(led_pin,HIGH);}

    
    void loop(){
      digitalWrite(relay_pin,HIGH);
      delay(5000);
      digitalWrite(relay_pin,LOW);
      delay(5000);
    }
