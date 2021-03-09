
uint32_t tempo; 
int configTempo; 

void setup() 
{
Serial.begin(115200); // opens serial port, sets data rate to 9600 bps
pinMode(13,OUTPUT);
pinMode(12,OUTPUT);
pinMode(8,INPUT_PULLUP);
}

void loop() 
{
tempo = millis()%configTempo;
 
if(tempo == 0)
{
  Serial.print("temps \n");
  delay(10);
}



 
} 

  
