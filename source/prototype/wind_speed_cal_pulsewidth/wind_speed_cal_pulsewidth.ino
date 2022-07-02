#define WIND_SPEED_PIN 39

int cal_factor = 585000;

void setup() {
  Serial.begin(115200);
  pinMode(WIND_SPEED_PIN, INPUT);

}

void loop() {
  unsigned long timeout = 1000000;
  long avg = 0;
  long mph = 0;
  int count = 2;
  
  if (Serial.available())
  {
    int in = Serial.parseInt();
    if (in > 0)
    {
      cal_factor = in;
    }
    
  }
  for(int i = 0; i < count; i++)
  {
    avg += pulseIn(WIND_SPEED_PIN, LOW, timeout);
  }
  avg /= count;
//  int pwm_value = pulseIn(WIND_SPEED_PIN, LOW, timeout);
  
  if (avg <= 0.0)
  {
    mph = 0;
  }
  else
  {
    mph = cal_factor / avg;
  }
  Serial.print("Calibration Factor: ");
  Serial.println(cal_factor);
  Serial.print("MPH: ");
  Serial.println(mph);
  Serial.print("ADC Value: ");
  Serial.println(avg);
  Serial.println("");
  delay(500);
}
