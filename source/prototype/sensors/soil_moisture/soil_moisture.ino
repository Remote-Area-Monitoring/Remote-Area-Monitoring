#define SOIL_PIN 36

int getSoilMoisture()
{
  int limit = 10;
  int avg = 0;
  for (int i = 0; i < limit; i++)
  {
    avg += analogRead(SOIL_PIN);
    delay(5);
  }
  avg /= limit;
  return avg;
}

void setup() 
{
  Serial.begin(115200);
  pinMode(SOIL_PIN, INPUT);
}

void loop() 
{
  Serial.println(getSoilMoisture());
  delay(1000);
}
