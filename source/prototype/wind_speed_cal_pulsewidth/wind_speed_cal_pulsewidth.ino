#define WIND_SPEED_PIN 39

void setup() {
  Serial.begin(115200);
  pinMode(WIND_SPEED_PIN, INPUT);

}

void loop() {
  unsigned long timeout = 1000000;
  long avg = 0;
  long mph = 0;
  int count = 3;
  for(int i = 0; i < count; i++)
  {
    avg += pulseIn(WIND_SPEED_PIN, LOW, timeout);
    delay(100);
  }
  avg /= count;
//  int pwm_value = pulseIn(WIND_SPEED_PIN, LOW, timeout);
  Serial.println(avg);
  if (avg <= 0.0)
  {
    mph = 0;
  }
  else
  {
    mph = 440000 / avg;
  }
  Serial.println(mph);
  delay(500);
}
