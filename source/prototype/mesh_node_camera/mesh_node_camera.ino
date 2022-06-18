#include <Wire.h>
#include <Adafruit_Sensor.h>
#include <Adafruit_BME280.h>
#include <Adafruit_CCS811.h>
#include <Adafruit_INA219.h>
#include <QMC5883LCompass.h>
#include <painlessMesh.h>
#include <DallasTemperature.h>
#include <ArduCAM.h>
#include <SPI.h>
#include "memorysaver.h"`
//#include <ArduinoJson.h>

#define   MESH_PREFIX     "ram"
#define   MESH_PASSWORD   "SeniorDesign1"
#define   MESH_PORT       5555

#define WIND_SPEED_PIN 39
#define WIND_DIR_PIN 34
#define SOIL_PIN 36
#define DS18_PIN 17
#define CAMERA_CS 5

Scheduler userScheduler;
painlessMesh mesh;

#if !(defined OV2640_MINI_2MP_PLUS)
  #error Please select the hardware platform and camera module in the ../libraries/ArduCAM/memorysaver.h file
#endif

ArduCAM myCAM( OV2640, CAMERA_CS );
uint8_t read_fifo_burst(ArduCAM myCAM);

bool is_header = false;
int mode = 0;
uint8_t start_capture = 0;

//DynamicJsonDocument pixelData(16384);
StaticJsonDocument<25000> pixelData;
JsonArray pixels = pixelData.createNestedArray("pixels");

void send_pixel_stats(uint32_t from, int packetNumber);
int capture();
void send_pixel_packet(uint32_t from);


// Needed for painless library
void receivedCallback( uint32_t from, String &msg ) {
  Serial.printf("Received from %u msg=%s\n", from, msg.c_str());
  Serial.println(msg);
//  String message = (String)msg;
//  Serial.println(message);
  if (msg == "image")
  {
    Serial.println("Starting Capture");
    capture(from);
  }
//  else
//  {
//    mesh.sendSingle(from, allSensorDataString());
//  }
  
}


void setup() 
{
  uint8_t vid, pid;
  uint8_t temp;
  
  Wire.begin();
  Serial.begin(115200);
  
  pinMode(CAMERA_CS, OUTPUT);
  digitalWrite(CAMERA_CS, HIGH);
  SPI.begin();

  //Reset the CPLD
  myCAM.write_reg(0x07, 0x80);
  delay(100);
  myCAM.write_reg(0x07, 0x00);
  delay(100);

  while(1)
  {
    //Check if the ArduCAM SPI bus is OK
    myCAM.write_reg(ARDUCHIP_TEST1, 0x55);
    temp = myCAM.read_reg(ARDUCHIP_TEST1);
    if (temp != 0x55){
      Serial.println(F("ACK CMD SPI interface Error! END"));
      delay(1000);continue;
    }else{
      Serial.println(F("ACK CMD SPI interface OK. END"));break;
    }
  }

  #if defined (OV2640_MINI_2MP_PLUS)
    while(1)
    {
      //Check if the camera module type is OV2640
      myCAM.wrSensorReg8_8(0xff, 0x01);
      myCAM.rdSensorReg8_8(OV2640_CHIPID_HIGH, &vid);
      myCAM.rdSensorReg8_8(OV2640_CHIPID_LOW, &pid);
      if ((vid != 0x26 ) && (( pid != 0x41 ) || ( pid != 0x42 ))){
        Serial.println(F("ACK CMD Can't find OV2640 module! END"));
        delay(1000);continue;
      }
      else{
        Serial.println(F("ACK CMD OV2640 detected. END"));break;
      } 
    }
  #endif

  myCAM.set_format(JPEG);
  myCAM.InitCAM();
  myCAM.OV2640_set_JPEG_size(OV2640_640x480);
  delay(1000);
  myCAM.clear_fifo_flag();
  #if !(defined (OV2640_MINI_2MP_PLUS))
    myCAM.write_reg(ARDUCHIP_FRAMES,0x00);
  #endif


  mesh.setDebugMsgTypes( ERROR | STARTUP | CONNECTION );  // set before init() so that you can see startup messages
  mesh.init( MESH_PREFIX, MESH_PASSWORD, &userScheduler, MESH_PORT );
  mesh.onReceive(&receivedCallback);
}

void loop() 
{
  uint8_t temp = 0xff, temp_last = 0;
  bool is_header = false;

  mesh.update();

}

int capture(uint32_t from)
{
  myCAM.OV2640_set_Light_Mode(Auto);
  uint8_t temp = 0xff;
  uint8_t temp_last = 0;
  uint32_t length = 0;
  //Check if the ArduCAM SPI bus is OK
  myCAM.write_reg(ARDUCHIP_TEST1, 0x55);
  temp = myCAM.read_reg(ARDUCHIP_TEST1);
  if (temp != 0x55){
    Serial.println(F("ACK CMD SPI interface Error! END"));
    delay(1000);
  }else{
    Serial.println(F("ACK CMD SPI interface OK. END"));
  }
  temp = 0xff;
  myCAM.flush_fifo();
  myCAM.clear_fifo_flag();
  //Start capture
  Serial.println("Capture Start");
  myCAM.start_capture();
  delay(500);
  Serial.print("Status Bit:");
  Serial.println(myCAM.get_bit(ARDUCHIP_TRIG, CAP_DONE_MASK));

  if (myCAM.get_bit(ARDUCHIP_TRIG, CAP_DONE_MASK))
  {
    Serial.println(F("ACK CMD CAM Capture Done. END"));delay(50);
    temp = 0;
    length = myCAM.read_fifo_length();
    Serial.println(length, DEC);
    if (length >= MAX_FIFO_SIZE) //512 kb
    {
      Serial.println(F("ACK CMD Over size. END"));
      return 0;
    }
    if (length == 0 ) //0 kb
    {
      Serial.println(F("ACK CMD Size is 0. END"));
      return 0;
    }
    myCAM.CS_LOW();
    myCAM.set_fifo_burst();//Set fifo burst mode
    temp =  SPI.transfer(0x00);
    length --;
    int count = 0;
    int packetNumber = 0;
    initialize_pixel_data(0);
    while ( length-- )
    {
      if (count >= 1000)
      {
        send_pixel_packet(from);
        packetNumber++;
        initialize_pixel_data(packetNumber);
        count = 0;
      }
      temp_last = temp;
      temp =  SPI.transfer(0x00);
      if (is_header == true)
      {
//        Serial.write(temp);
        pixels.add(temp);
        count++;
      }
      else if ((temp == 0xD8) & (temp_last == 0xFF))
      {
        is_header = true;
//        Serial.println(F("ACK IMG END"));
//        Serial.write(temp_last);
        pixels.add(temp_last);
        count++;
//        Serial.write(temp);
        pixels.add(temp);
        count++;
      }
      if ( (temp == 0xD9) && (temp_last == 0xFF) ) //If find the end ,break while,
      {
        send_pixel_packet(from);
        send_pixel_stats(from, packetNumber);
        break;
      }
      delayMicroseconds(15);
    }
    myCAM.CS_HIGH();
    is_header = false;
    myCAM.clear_fifo_flag();
  }
  return 1;
}


void initialize_pixel_data(long packetNumber)
{
  pixelData.clear();
  pixelData["node_id"] = mesh.getNodeId();
  pixelData["packet_number"] = packetNumber;
  pixels = pixelData.createNestedArray("pixels");
}


void send_pixel_packet(uint32_t from)
{
  String str = "";
  serializeJson(pixelData, str);
  Serial.println(str);
  mesh.sendSingle(from, str);
}

void send_pixel_stats(uint32_t from, int packetNumber)
{
  String message = "{\"node_id\": ";
  message = message + mesh.getNodeId() + ", \"total_packets_sent\": " + packetNumber + "}";
  mesh.sendSingle(from, message);
}
