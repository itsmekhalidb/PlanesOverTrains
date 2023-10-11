// Include library code
#include <Wire.h> 
#include <LiquidCrystal_I2C.h>

LiquidCrystal_I2C lcd1(0x20,20,4);
String incomingData;


int Detect_LED = 2;
int Red_LED = 3;
int Green_LED = 4;
int Super_Green = 5;

void Transmitter(){

}

void Receiver() {
  if (Serial.available() > 0){
    incomingData = Serial.readStringUntil('\n');
  }

  if (incomingData.substring(0,1).equals("1")){
    digitalWrite(Detect_LED, HIGH);
    digitalWrite(Red_LED, LOW);
    digitalWrite(Green_LED, LOW);
    digitalWrite(Super_Green, LOW);
  }
  else if (incomingData.substring(0,1).equals("0")) digitalWrite(Detect_LED, LOW);
  
  if(incomingData.substring(1,2).equals("1")){
    lcd1.clear();
    lcd1.setCursor(0,0);
    lcd1.print("Commanded Speed:");
    lcd1.setCursor(0,1);
    lcd1.print(incomingData.substring(5,incomingData.length()));
  }
  
  if(incomingData.substring(2,3).equals("1")){
    lcd1.clear();
    lcd1.setCursor(0,0);
    lcd1.print("Switch:");
    lcd1.setCursor(0,1);
    lcd1.print(incomingData.substring(5,incomingData.length()));
  }

  if(incomingData.substring(3,4).equals("1")){
    lcd1.clear();
    lcd1.setCursor(0,0);
    lcd1.print("Light:");
    lcd1.setCursor(0,1);
    lcd1.print(incomingData.substring(5,incomingData.length()));
    if(incomingData.substring(4,5).equals("0")){
      digitalWrite(Red_LED, HIGH);
    }
    else if(incomingData.substring(4,5).equals("1")){
      digitalWrite(Red_LED, HIGH);
      digitalWrite(Green_LED, HIGH);
    }
    else if(incomingData.substring(4,5).equals("2")){
      digitalWrite(Red_LED, HIGH);
      digitalWrite(Green_LED, HIGH);
      digitalWrite(Super_Green, HIGH);
    }
  }
}

  void setup(){
    Serial.begin(9600);
    pinMode(2, OUTPUT);
    pinMode(3, OUTPUT);
    pinMode(4, OUTPUT);
    pinMode(5, OUTPUT);

  }

  void loop(){
    lcd1.init();
    lcd1.backlight();
    Receiver();
    delay(500);
  }

