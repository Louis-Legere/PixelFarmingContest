#include "Arduino_EMBRYO_2.h"


const int BackwardPin = 40;     // Backward Button X-axis
const int ForwardPin  = 40;     // Forward Button X-axis
const int startPin = 40;         // Start Button
const int emergencyPin = 40;    // Emergency Button
const int FarEndstop = 40;       // Far From Home endstop X-axis


#define motor01      1

const int enablePin1 = 38;      // Enable Pin
const int DirPin1 = A1;         // Direction Pin for motor01
const int PulPin1 = A0;         // Step Pin for motor01

const int min1 = 3;        // Endstop 1


#define motor02      2

const int enablePin2 = A2;      // Enable Pin
const int DirPin2 = A7;         // Direction Pin for motor01
const int PulPin2 = A6;         // Step Pin for motor01

const int max1 = 2;        // Endstop 1


#define motor03      3

const int enablePin3 = A8;      // Enable Pin
const int DirPin3 = 48;         // Direction Pin for motor01
const int PulPin3 = 46;         // Step Pin for motor01

const int min2 = 14;        // Endstop 2


#define motor04      4

const int enablePin4 = 24;      // Enable Pin
const int DirPin4 = 28;         // Direction Pin for motor01
const int PulPin4 = 26;         // Step Pin for motor01

const int max2 = 15;        // Endstop 2
const int min3 = 18;        // Endstop 3
const int max4 = 19;        // Endstop 4

long steps = 0;

/* Construct object, Embryo(Axis, Enable Pin, Direction Pin, Pulse Pin, Endstop Home, Endstop Far, Forward Button, Backward Button, Start Button, Emergency) */

StepMotor box[] =  {StepMotor (motor01, enablePin1, DirPin1, PulPin1, min1, FarEndstop, ForwardPin, BackwardPin, startPin, emergencyPin), 
                    StepMotor (motor02, enablePin2, DirPin2, PulPin2, max1, FarEndstop, ForwardPin, BackwardPin, startPin, emergencyPin),
                    StepMotor (motor03, enablePin3, DirPin3, PulPin3, min2, FarEndstop, ForwardPin, BackwardPin, startPin, emergencyPin),
                    StepMotor (motor04, enablePin4, DirPin4, PulPin4, max2, FarEndstop, ForwardPin, BackwardPin, startPin, emergencyPin)};

void setup() {

  Serial.begin(9600);         // Configure and start Serial Communication

  for (int i = 0; i< box.length(); i++){
    box[i].begin();
    box[i].startWithoutHoming();
    
    while(!box[i].readEndstopHome()){
      box[i].moveBackward();
    } 
  }
  
  
  Serial.println("To start, send any key to serial ...");

  Serial.println ("Homing axis " + String(_id));



  // Without this instruction the motor will move after the upload (It is dangerous)
  while((Serial.available() <= 0)){};
}

void loop() {
  // put your main code here, to run repeatedly:

}
