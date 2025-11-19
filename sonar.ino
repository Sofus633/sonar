const int led_pin = 13;
const int trig_pin = 8;
const int echo_pin = 9;
int angle = 0;
int precision = 1;
int count = 0;

int max_rota = 180;

int numerpoint = max_rota / (max_rota / precision);

int **points = malloc(sizeof(2 * (sizeof(int)) * numerpoint));

void blink_led()
{
  digitalWrite(led_pin, HIGH);
  delay(10);
  digitalWrite(led_pin, LOW);
}

int get_distance(void)
{
  //sending wave
  digitalWrite(trig_pin, HIGH);
  delay(10);
  digitalWrite(trig_pin, LOW);

  //recieving
  int timing = pulseIn(echo_pin, HIGH);
  return (timing * 0.034) / 2;
}

float radiants(int deg)
{
  return (deg * 71) / 4068;
}

int get_x(int distance,int angle)
{
  return (cos(radiants(angle)) * distance);
}
int get_y(int distance,int angle)
{
  return (sin(radiants(angle)) * distance);
}

void setup() {

  Serial.begin(9600);
  pinMode(echo_pin, INPUT);
  pinMode(trig_pin, OUTPUT);
  pinMode(led_pin, OUTPUT);
}

void loop() {
  angle += precision;
  int distance = get_distance();
  Serial.println("Entry Start :");
  Serial.print(get_x(distance, angle));
  Serial.print(", ");
  Serial.println(get_y(distance, angle));
  Serial.println(angle);

  
  blink_led();
  if (angle > 180 || angle < 0)
  {
    count += 1;
    precision *= -1;
  }
  
  if (count >= 2)
  {
    free(points);
    Serial.println("END");
    exit(0);
  }
}
