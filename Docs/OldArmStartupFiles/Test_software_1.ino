#include <SPI.h>
#include <Controllino.h>
#include <AccelStepper.h>
#include "c_statehandler.h"

c_statehandler statehandler;

enum e_states 
{
  INIT, HOMING_STEP1, HOMING_STEP2, IDLE
} ;

enum e_states armstate;

//Defining Pinnames for easier programming
int Stepper1PUL = CONTROLLINO_D0;
int Stepper1DIR = CONTROLLINO_D1;
int Stepper1ENA = CONTROLLINO_D2; // its actaualy recomended to not connect Enable at all -> for this reason this pin will not be used further in this sketch
int Stepper1ALM = CONTROLLINO_D3;
int Stepper1ESO = CONTROLLINO_D9;
int Stepper1ESI = CONTROLLINO_D10;
int Stepper1BRK = CONTROLLINO_RELAY_06;
bool Stepper1Homed;

int Stepper2PUL = CONTROLLINO_D4;
int Stepper2DIR = CONTROLLINO_D5;
int Stepper2ENA = CONTROLLINO_D6; // its actaualy recomended to not connect Enable at all -> for this reason this pin will not be used further in this sketch
int Stepper2ALM = CONTROLLINO_D7;
int Stepper2ESO = 42;
int Stepper2ESI = CONTROLLINO_D11;
int Stepper2BRK = CONTROLLINO_RELAY_07;
bool Stepper2Homed;


AccelStepper step1(1, Stepper1PUL, Stepper1DIR);
AccelStepper step2(1, Stepper2PUL, Stepper2DIR);



void setup() {
  // put your setup code here, to run once:
  pinMode(Stepper1PUL, OUTPUT);
  pinMode(Stepper1DIR, OUTPUT);
  pinMode(Stepper1ESO, OUTPUT);
  pinMode(Stepper1BRK, OUTPUT);

  pinMode(Stepper1ALM, INPUT);
  pinMode(Stepper1ESI, INPUT);


  pinMode(Stepper2PUL, OUTPUT);
  pinMode(Stepper2DIR, OUTPUT);
  pinMode(Stepper2ESO, OUTPUT);
  pinMode(Stepper2BRK, OUTPUT);

  pinMode(Stepper2ALM, INPUT);
  pinMode(Stepper2ESI, INPUT);

  digitalWrite(Stepper1ESO, true);
  digitalWrite(Stepper2ESO, true);

  Serial.begin(115200);
  step1.setMaxSpeed(3000);
  step1.setSpeed(0);
  step1.setAcceleration(1000);

  step2.setMaxSpeed(3000);
  step2.setSpeed(0);
  step2.setAcceleration(1000);

}

void loop() {
  // put your main code here, to run repeatedly:
  switch(armstate)
    {
        case INIT:
          digitalWrite(Stepper1BRK, true);
          digitalWrite(Stepper2BRK, true);

          if(statehandler.elapsedtime() > 10)
          {
          armstate = HOMING_STEP1 ;
          statehandler.setNextState(armstate);
          }
        break;

        case HOMING_STEP1:
        if(statehandler.onentry == true)
          {
              step1.setSpeed(1000);
              step2.setSpeed(-1000);
          }

          step1.runSpeed();
          step2.runSpeed();

          Stepper1Homed = digitalRead(Stepper1ESI);

          if(Stepper1Homed == true)
          {
            step1.setSpeed(0);
            step2.setSpeed(0);
            step1.runSpeed();
            step2.runSpeed();
            step1.setCurrentPosition(0);
            armstate = HOMING_STEP2;
            statehandler.setNextState(armstate);
          }
        break;

        case HOMING_STEP2:
          if(statehandler.onentry == true)
            {
              step1.setSpeed(-1000);
              step2.setSpeed(1000);
            }

          step1.runSpeed();
          step2.runSpeed();

          Stepper2Homed = digitalRead(Stepper2ESI);

          if(Stepper2Homed == true)
          {
            step1.setSpeed(0);
            step2.setSpeed(0);
            step1.runSpeed();
            step2.runSpeed();
            step2.setCurrentPosition(0);
            armstate = IDLE;
            statehandler.setNextState(armstate);
          }
        break;

        case IDLE:
         Serial.println(step1.currentPosition());

         
        break;

    }
    statehandler.handlestate();
}


   
  




