#include <Wire.h>
#include <Adafruit_INA219.h>
#include <ArduinoJson.h>
#include <painlessMesh.h>


#define   MESH_PREFIX     "ram"
#define   MESH_PASSWORD   "SeniorDesign1"
#define   MESH_PORT       5555


Scheduler userScheduler;
painlessMesh mesh;

Adafruit_INA219 current;

DynamicJsonDocument doc(2048);

String getCurrent()
{
  doc["bus_voltage"] = current.getBusVoltage_V();
  doc["shunt_voltage"] = current.getShuntVoltage_mV();
  doc["current"] = current.getCurrent_mA();
  doc["power"] = current.getPower_mW();
  String str = "";
  serializeJson(doc, str);
  return str;
}

// Needed for painless library
void receivedCallback( uint32_t from, String &msg ) {
  Serial.printf("startHere: Received from %u msg=%s\n", from, msg.c_str());
  mesh.sendBroadcast(getCurrent());
}

void setup() {
  Serial.begin(115200);
    
  mesh.setDebugMsgTypes( ERROR | STARTUP | CONNECTION );  // set before init() so that you can see startup messages

  mesh.init( MESH_PREFIX, MESH_PASSWORD, MESH_PORT );
  mesh.onReceive(&receivedCallback);

  current.begin();
}

void loop() {
  mesh.update();
}
