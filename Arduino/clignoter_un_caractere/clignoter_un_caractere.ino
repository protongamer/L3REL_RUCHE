bool BT1;
bool act = 0;
bool state = 0;


void setup() {
  // put your setup code here, to run once:
pinMode(7,INPUT_PULLUP);
pinMode(13,OUTPUT);
}

void loop() {
  // put your main code here, to run repeatedly:
BT1 = !digitalRead(7);

if(BT1 == 1){
act = 1;  
}

if(act == 1){
  state = !state;
}


digitalWrite
(13,state);
delay(1000);
}
