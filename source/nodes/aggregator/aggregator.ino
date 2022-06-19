#include <ArduinoJson.h>
#include <painlessMesh.h>

#define   MESH_PREFIX     "ram"
#define   MESH_PASSWORD   "SeniorDesign1"
#define   MESH_PORT       5555

DynamicJsonDocument command(512);
DynamicJsonDocument newNode(128);
DynamicJsonDocument received(4096);

Scheduler userScheduler;
painlessMesh mesh;
void sendMessage();
Task taskSendMessage(TASK_SECOND * 1, TASK_FOREVER, &sendMessage);


void parseCommand()
{
  auto parse_failed = deserializeJson(command, Serial);

  if (parse_failed)
  {
    command["error"] = parse_failed.c_str();
  }
  else
  {
    command["size"] = command.size();
  }
}


void sendMessage()
{
//  String message = "Echo sent from aggregator. Aggregator ID: ";
//  message += mesh.getNodeId();
//  mesh.sendBroadcast(message);
  // mesh.sendSingle(8043016, message);

  parseCommand();

  if (!command.containsKey("error"))
  {
    String message = command["message"];
    uint32_t nodeId = command["node_id"];

    if (nodeId == 0)
    {
      Serial.print(mesh.subConnectionJson());
      Serial.println("*");
    }
    else if (nodeId == 1)
    {
//      Serial.println("broadcasting: %s", String(command["message"]));
//      Serial.println(message);
      mesh.sendBroadcast(message);
    }
    else
    {
      mesh.sendSingle(nodeId, message);
    }
  }

  taskSendMessage.setInterval(TASK_SECOND * 1);
//  serializeJson(command, Serial);
//  Serial.println("*");
}

// Needed for painless library
void receivedCallback( uint32_t from, String &msg ) {
//  Serial.printf("startHere: Received from %u msg=%s\n", from, msg.c_str());
  Serial.printf("%s", msg.c_str());
  Serial.println("*");
}

void newConnectionCallback(uint32_t nodeId) {
    newNode["event_type"] = "new_connection";
    newNode["node_id"] = nodeId;
    serializeJson(newNode, Serial);
    Serial.println("*");
}


void setup()
{
  Serial.begin(115200);

  mesh.init( MESH_PREFIX, MESH_PASSWORD, &userScheduler, MESH_PORT );
  mesh.setRoot(true);
  mesh.setContainsRoot(true);
  mesh.onReceive(&receivedCallback);
  mesh.onNewConnection(&newConnectionCallback);

  userScheduler.addTask( taskSendMessage );
  taskSendMessage.enable();
}

void loop()
{
  mesh.update();
}
