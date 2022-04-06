void setup() {
  Serial.begin(115200);
  
}

void loop() {
  if (Serial.available())
  {
    uint8_t temp = Serial.read();
    Serial.write(temp);
  }

}
