#define WIND_DIR_PIN 34

int cal_factor = 585000;

void setup() 
{
  Serial.begin(115200);
  pinMode(WIND_DIR_PIN, INPUT);

}

void loop() {
  unsigned long timeout = 1000000;
  long avg = 0;
  long dir_degrees = 0;
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
    avg += pulseIn(WIND_DIR_PIN, LOW, timeout);
  }
  avg /= count;
//  int pwm_value = pulseIn(WIND_SPEED_PIN, LOW, timeout);
  
  if (avg <= 0.0)
  {
    dir_degrees = 0;
  }
  else
  {
    dir_degrees = 360 - ((avg - 101) / 2.23);
  }
  Serial.print("Calibration Factor: ");
  Serial.println(cal_factor);
  Serial.print("Degrees: ");
  Serial.println(dir_degrees);
  Serial.print("ADC Value: ");
  Serial.println(avg);
  Serial.println("");
  delay(500);
}
