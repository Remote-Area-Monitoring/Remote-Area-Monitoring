#include <Wire.h>
#include <Adafruit_Sensor.h>
#include <Adafruit_BME280.h>
#include <Adafruit_CCS811.h>
#include <Adafruit_INA219.h>
#include <QMC5883LCompass.h>
#include <painlessMesh.h>

#define   MESH_PREFIX     "ram"
#define   MESH_PASSWORD   "SeniorDesign1"
#define   MESH_PORT       5555

#define WIND_SPEED_PIN 0
#define WIND_DIR_PIN 0

Adafruit_INA219 ina;
Adafruit_BME280 bme;
Adafruit_CCS811 ccs;
QMC5883LCompass compass;
Scheduler userScheduler;
painlessMesh mesh;

DynamicJsonDocument data(4096);

volatile unsigned int pulses = 0;
const float WIND_SPEED_CONST = 1.0;

const float WIND_DIR_MIN = 1000.0;
const float WIND_DIR_MAX = 4000.0;
const float WIND_DIR_DEG_PER_COUNT = 1.0;

void getNodeIdData();
void getPowerData();
void getAtmosphericData();
void getAirQualityData();
void getWindSpeed();
void getWindDirection();
void getCompassData();

String allSensorDataString();

// Needed for painless library
void receivedCallback( uint32_t from, String &msg ) {
  Serial.printf("Received from %u msg=%s\n", from, msg.c_str());
  mesh.sendSingle(from, allSensorDataString());
}


void setup() 
{
  Serial.begin(115200);

  ina.begin();
  bme.begin(0x76); // pass the default address otherwise the sensor is not found
  ccs.begin();
  compass.init();

  pinMode(WIND_SPEED_PIN, INPUT);
  attachInterrupt(0, countPulses, RISING);

  pinMode(WIND_DIR_PIN, INPUT);

  mesh.setDebugMsgTypes( ERROR | STARTUP | CONNECTION );  // set before init() so that you can see startup messages
  mesh.init( MESH_PREFIX, MESH_PASSWORD, MESH_PORT );
  mesh.onReceive(&receivedCallback);
}


void loop() 
{
  mesh.update();
}


String allSensorDataString()
{
  getNodeIdData();
  getPowerData();
  getAtmosphericData();
  getAirQualityData();
  getWindSpeed();
  getWindDirection();
  getCompassData();

  String str = "";
  serializeJson(data, str);
  return str;
}

void getNodeIdData()
{
  data["node_id"] = mesh.getNodeId();
}

void getPowerData()
{
  data["bus_voltage_V"] = ina.getBusVoltage_V();
  data["shunt_voltage_mV"] = ina.getShuntVoltage_mV();
  data["current_mA"] = ina.getCurrent_mA();
  data["power_mW"] = ina.getPower_mW();
}

void getAtmosphericData()
{
  data["air_temperature_C"] = bme.readTemperature();
  data["humidity"] = bme.readHumidity();
  data["air_pressure_Pa"] = bme.readPressure();
}

void getAirQualityData()
{
  ccs.readData();
  data["co2_ppm"] = ccs.geteCO2();
  data["tvoc_ppb"] = ccs.getTVOC();
}

void countPulses()
{
  pulses++;
}

void getWindSpeed()
{
  pulses = 0;
  interrupts();
  delay(1000);
  noInterrupts();
  float windSpeed = pulses / WIND_SPEED_CONST;
  data["wind_speed_mph"] = windSpeed;
}

void getWindDirection()
{
  float averageCounts = 0.0;
  int numPolls = 5;

  for (int i = 0; i < numPolls; i++)
  {
    averageCounts += analogRead(WIND_DIR_PIN);
    delay(5);
  }
  
  averageCounts /= numPolls;
  averageCounts = averageCounts - WIND_DIR_MIN;
  if (averageCounts < 0)
  {
    averageCounts = 0;
  }

  float windDirection = averageCounts / WIND_DIR_DEG_PER_COUNT;
  data["wind_direction"] = windDirection;
}

void getCompassData()
{
  char direction[3];
  compass.read();
  data["azimuth"] = compass.getAzimuth(); 
  data["bearing"] = compass.getBearing(data["azimuth"]); // This will divide the 360 range of the compass into 16 parts and return a value of 0-15 in clockwise order
  compass.getDirection(direction, data["azimuth"]); // NSEW letters
  data["direction"] = String(direction);
}