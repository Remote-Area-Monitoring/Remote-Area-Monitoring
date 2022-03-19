#include <QMC5883LCompass.h>

QMC5883LCompass compass;

void setup() 
{
  Serial.begin(115200);
  compass.init();
}

void loop() 
{
  Serial.println(getDegrees());
  delay(1000);
}


int getDegrees()
{
  compass.read();
  return compass.getAzimuth();
}