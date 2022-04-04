#define WIND_SPEED_PIN 39

volatile unsigned int pulses = 0;

void countPulses()
{
  pulses++;
}

float getRPM()
{
  pulses = 0;
  interrupts();
  delay(1000);
  noInterrupts();
  float rpm = (pulses / 4.2998) * 60;
//  double rpm = pulses;
  return rpm;
}

void setup() 
{
  Serial.begin(115200);
  pinMode(WIND_SPEED_PIN, INPUT);
  attachInterrupt(WIND_SPEED_PIN, countPulses, RISING);
}

void loop() 
{
  Serial.println(getRPM());
  delay(500);
}
