/*
This is the arduino code for the PiHat.
 It consists of a GYML8511 UV sensor and a TGS2602 air quality sensor.
 
 The GYML8511 is connected to the arduino board as follows:
 VIN = NOT CONNECTED
 3.3V = 3.3V
 GND = GND
 OUT = A0
 EN = 3.3v
 3.3V = A1
 
 The 3.3V connected to EN and A1 is all from the original 3.3V input on the breadboard.
 The A1 is used as an accurate reference level to campare with the reading from the sensor to get a true-to-life reading.
 
 The TGS2602 is connected as follows:
 Pin 1 = GND
 Pin 2 = GND + a 10K carbon film resistor
 Pin 3 = 5V
 Pin 4 = 5v
 */

//Hardware Pin Definitions
int UVOUT = A0;
int REF_3V3 = A1;
int gasSensor = A2;

int gasVal = 0;

void setup(){
  Serial.begin(9600);

  pinMode(UVOUT, INPUT);
  pinMode(REF_3V3, INPUT);
  pinMode(gasSensor, INPUT);
  //Serial.println("PiHat Ready to Go!");

}

void loop(){
  int uvLevel = averageAnalogRead(UVOUT);
  int refLevel = averageAnalogRead(REF_3V3);

  //Use the 3.3V power pin as a reference to get a very accurate output value from sensor
  float outputVoltage = 3.3 / refLevel * uvLevel;

  float uvIntensity = mapfloat(outputVoltage, 0.99, 2.8, 0.0, 15.0); //Convert the voltage to a UV intensity level
  /*
  Serial.print("Output: ");
  Serial.print(refLevel);

  Serial.print(" / ML8511 output: ");
  Serial.print(uvLevel);

  Serial.print(" / ML8511 voltage: ");
  Serial.print(outputVoltage);
  
  Serial.print(" / UV Intensity (mW/cm^2): ");
  */
  //Serial.print("UV Intensity (mw/cm^2): ");
  Serial.println(uvIntensity);

  //Serial.println();

  gasVal = analogRead(gasSensor);
  //Serial.print("Gas Value: ");
  Serial.println(gasVal);
  //Serial.println();

  delay(1000);
}

//Takes an average of readings on a given pin
//Returns the average
int averageAnalogRead(int pinToRead)
{
  byte numberOfReadings = 8;
  unsigned int runningValue = 0; 

  for(int x = 0 ; x < numberOfReadings ; x++)
    runningValue += analogRead(pinToRead);
  runningValue /= numberOfReadings;

  return(runningValue);  
}

//The Arduino Map function but for floats
//From: http://forum.arduino.cc/index.php?topic=3922.0
float mapfloat(float x, float in_min, float in_max, float out_min, float out_max)
{
  return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min;
}


