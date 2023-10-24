#include <Stepper.h>
int pin;
#define IN1 14 // D5
#define IN2 12 // D6
#define IN3 13 // D7
#define IN4 15 // D8
#define LOCK 5 // D1
/*
 Stepper Motor Control - one revolution

 This program drives a unipolar or bipolar stepper motor.
 The motor is attached to digital pins 8 - 11 of the Arduino.

 The motor should revolve one revolution in one direction, then
 one revolution in the other direction.


 Created 11 Mar. 2007
 Modified 30 Nov. 2009
 by Tom Igoe

 */

#include <Stepper.h>

const int stepsPerRevolution = 1500;//2000;  // change this to fit the number of steps per revolution
// for your motor

// initialize the stepper library on pins 8 through 11:
Stepper myStepper(stepsPerRevolution, IN1, IN2, IN3, IN4); //D5 D6 D7 D8

void setup() {
  // set the speed at 60 rpm:
  myStepper.setSpeed(60);
  // initialize the serial port:
  Serial.begin(9600);
  //pinMode(2, INPUT);
}

void loop() {
  String data = "aaa";
 if (Serial.available() > 0) { //checking data availability
    Serial.println("Serial available");
    String data = Serial.readStringUntil('\n'); //reading line
    Serial.print("You sent me: "); //retransmitting
    Serial.println(data); //retransmitting 
    if (data == "couple") {      
      Serial.println("couple"); 
      couple();
      motorOff();
      }
    else if (data == "decouple"){
      Serial.println("Decouple"); 
      decouple();
      motorOff();
      }

  }



}

void forward() {
  myStepper.step(1.06 * stepsPerRevolution);
}

void backward() {
  myStepper.step(-1.06 * stepsPerRevolution);
}


void couple() {
  for(int i=0; i<6; i++) {
    forward();
    Serial.println(i); }
    myStepper.step(1.06 * 750);
}

void decouple() {

  for(int i=0; i<6; i++){
     backward();
    Serial.println(i);
  }
   myStepper.step(-1.06 * 750);

}
void motorOff() {
  digitalWrite(IN1, LOW);
  digitalWrite(IN2, LOW);
  digitalWrite(IN3, LOW);
  digitalWrite(IN4, LOW);
}
