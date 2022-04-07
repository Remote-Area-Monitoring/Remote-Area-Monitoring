#include <Wire.h>
#include <Adafruit_Sensor.h>
#include <Adafruit_CCS811.h>
#include <ArduinoJson.h>

Adafruit_CCS811 ccs;

DynamicJsonDocument data(1024);

void getAirQualityData()
{
  ccs.readData();
  data["co2_ppm"] = ccs.geteCO2();
  data["tvoc_ppb"] = ccs.getTVOC();
}

void setup() 
{
  Serial.begin(115200);
  ccs.begin();
}

void loop() 
{
  getAirQualityData();
  String str = "";
  serializeJson(data, str);
  Serial.println(str);
  delay(1000);
}
