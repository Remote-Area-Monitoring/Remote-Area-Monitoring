#define WIND_SPEED_PIN 39

void setup() {
  Serial.begin(115200);
  pinMode(WIND_SPEED_PIN, INPUT);

}

void loop() {
  unsigned long timeout = 1000000;
  int pwm_value = pulseIn(WIND_SPEED_PIN, LOW, timeout);
  Serial.println(pwm_value);
  delay(500);
}
