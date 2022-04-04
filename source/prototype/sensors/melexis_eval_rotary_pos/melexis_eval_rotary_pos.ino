#define WIND_DIR_PIN 34

void setup() 
{
  Serial.begin(115200);
  pinMode(WIND_DIR_PIN, INPUT);
}

void loop() 
{
  Serial.println(analogRead(WIND_DIR_PIN));
  delay(1000);
}
