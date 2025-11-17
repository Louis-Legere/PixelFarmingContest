#include <Servo.h>

#define LED1 13      // use onboard LED instead of D2
#define SERVO_PIN 9  // servo control pin (typical choice for Uno)

unsigned long previousMillis = 0;
const long interval = 500;  // blink every 0.5s
bool ledState = LOW;

Servo myservo;

void setup() {
  Serial.begin(9600);
  pinMode(LED1, OUTPUT);

  myservo.attach(SERVO_PIN);  // attach servo to D9
  myservo.write(90);          // start at midpoint
}

void loop() {
  // Blink LED without blocking servo
  unsigned long currentMillis = millis();
  if (currentMillis - previousMillis >= interval) {
    previousMillis = currentMillis;
    ledState = !ledState;
    digitalWrite(LED1, ledState);
  }

  // Sweep servo 0 → 180 → 0
  for (int pos = 0; pos <= 120; pos++) {
    myservo.write(pos);

    // print every 10 degrees
    if (pos % 10 == 0) {
      Serial.print("Servo position: ");
      Serial.println(pos);
    }

    delay(10);
  }

  for (int pos = 120; pos >= 0; pos--) {
    myservo.write(pos);

    if (pos % 10 == 0) {
      Serial.print("Servo position: ");
      Serial.println(pos);
    }

    delay(10);
  }
}