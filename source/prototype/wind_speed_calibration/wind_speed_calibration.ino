#define WIND_SPEED_PIN 39

volatile unsigned int pulses = 0;
float WIND_SPEED_CONST = 1.0;


void countPulses();
float getWindSpeed();
float getAveragePulses();
float calculatedSpeed();


void setup() 
{
  Serial.begin(115200);
  
  pinMode(WIND_SPEED_PIN, INPUT);
  attachInterrupt(WIND_SPEED_PIN, countPulses, FALLING);
}

void loop() 
{
//  if (Serial.available())
//  {
//    float input = Serial.parseFloat();
//    if (!(input <= 0.0))
//    {
//      Serial.print("Setting new constant: ");
//      Serial.println(input);
//      WIND_SPEED_CONST = input;
//    }
//  }
//  Serial.print("Averaged Pulses: ");
//  Serial.println(getAveragePulses());
//  Serial.print("Calculated Speed: ");
//  Serial.println(calculatedSpeed());
//  Serial.print("Calc Pulses: ");
//  Serial.println(pulses);
//  Serial.println("");
//  Serial.print("Uncalculated Speed: ");
//  Serial.println(getWindSpeed());
//  Serial.print("Speed Pulses: ");
//  Serial.println(pulses);
//  Serial.println("");
  calculatedSpeed();
  delay(1000);
}

void countPulses()
{
  pulses++;
}

float getAveragePulses()
{
  float avg = 0;
  for (int i = 0; i < 5; i++)
  {
    pulses = 0;
    interrupts();
    delay(1000);
    noInterrupts();
    avg += pulses;
  }
  return avg / 5;
}

float getWindSpeed()
{
  pulses = 0;
  interrupts();
  delay(5000);
  noInterrupts();
  if (pulses <= 0.0)
  {
    pulses = 1.0;
  }
  float windSpeed = WIND_SPEED_CONST / pulses;
  return windSpeed;
}

float calculatedSpeed()
{
  pulses = 0;
  interrupts();
  delay(1000);
  noInterrupts();
  float windSpeed = pulses * 3.1415 *2 * (4.9/(5280*12));
  Serial.print("Calculated Speed: ");
  Serial.println(windSpeed);
  Serial.print("Calc Pulses: ");
  Serial.println(pulses);
  Serial.println("");
  return windSpeed;
}
