#include <Wire.h>

#include <Wire.h>
#include "SHT2x.h"

const int analogInPin = A0;  // Analog input pin for Apogee 515

int period = 1000;
unsigned long time_now = 0;

SHT2x SHT2x;

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600); //Start the Serial Port at 9600 baud (default)
  Wire.begin();
}

void loop() {
  if(millis() > time_now + period){
        time_now = millis();

      // read the input from analog pin:
      int sensorValue = analogRead(analogInPin);
      
      // Convert the analog reading (which goes from 0 - 1023) to a voltage (0 - 5V):
      float SQ515a = sensorValue * (5.0 / 1023.0);
      
      //Multiply this calibration factor by the measured voltage to convert sensor output to PPFD 
      float SQ515b = SQ515a * 2000;
      int SQ515 = int(SQ515b);
      
      float T = SHT2x.GetTemperature();
      float H = SHT2x.GetHumidity();
         
      Serial.print(T);
      Serial.print(",");
      Serial.print(H);
      Serial.print(",");
      Serial.print(SQ515);
      Serial.print(",");
      Serial.println();
  }

}
