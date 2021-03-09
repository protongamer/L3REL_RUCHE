
#include <Encoder.h>
#include <TimerOne.h>

int index_LED;


void setup()
{
  encoder.Timer_init();
  Serial.begin (115200); 
  
}
void loop()
{
    if (encoder.rotate_flag ==1)
  {
  Serial.println (index_LED);
    
    if (encoder.direct==1)
    {
      index_LED++;
      if (index_LED>23)
      index_LED=24;
    
    }
     else
     {
      index_LED--;
      if(index_LED<0)
      index_LED=0;
 
     }
    encoder.rotate_flag =0;
  }
}
