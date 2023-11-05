// Include library code
#include <Wire.h>
#include <LiquidCrystal_I2C.h>

LiquidCrystal_I2C lcd1(0x20, 20, 4);
String incomingData;



const int LIGHTNUMBER = 9;
const int SWITCHNUMBER = 3;

int Detect_LED = 2;
int Red_LED = 3;
int Green_LED = 4;
int Crossing_LED = 5;


struct Light{
  String name;
  int value;
};

struct Switch{
  String name;
  int value;
};


void Receiver() {
  if (Serial.available() > 0) {
    incomingData = Serial.readStringUntil('\n');
  }
  String detect = incomingData.substring(0,1);
  String block_number = incomingData.substring(1,5);
  String commanded_speed = incomingData.substring(5,7);
  String light_is = incomingData.substring(7,8);
  String light_state = incomingData.substring(8,9);
  String switch_is = incomingData.substring(9,10);
  String switch_state = incomingData.substring(10,11);
  String crossing_is = incomingData.substring(11,12);
  String crossing_state = incomingData.substring(12,13);

  if (detect.equals("1")) {
    digitalWrite(Detect_LED, HIGH);
    digitalWrite(Red_LED, LOW);
    digitalWrite(Green_LED, LOW);
    digitalWrite(Crossing_LED, LOW);
  }

    lcd1.clear();
    lcd1.setCursor(0, 0);
    lcd1.print("Block #: " + block_number);
    lcd1.setCursor(0, 1);
    lcd1.print("Commanded Speed: " + commanded_speed);

    if(light_is == "1"){
      if(light_state == "0"){
        digitalWrite(Red_LED, HIGH);
        digitalWrite(Green_LED, LOW);
      }
      else{
        digitalWrite(Red_LED, HIGH);
        digitalWrite(Green_LED, HIGH);
      }
    }
    if(switch_is == "1"){
      lcd1.setCursor(0,2);
      if(switch_state == "0"){
        lcd1.print("Switch: Left");
      }
      else{
        lcd1.print("Switch: Right");
      }
    }
    if(crossing_is == "1"){
      if(crossing_state == "1"){
        digitalWrite(Crossing_LED, HIGH);
      }
      else{
        digitalWrite(Crossing_LED, LOW);
      }
    }

  

  /*
  if (incomingData.substring(0, 1).equals("1")) {
    digitalWrite(Detect_LED, HIGH);
    digitalWrite(Red_LED, LOW);
    digitalWrite(Green_LED, LOW);
    digitalWrite(Super_Green, LOW);
  } else if (incomingData.substring(0, 1).equals("0")) digitalWrite(Detect_LED, LOW);

  if (incomingData.substring(1, 2).equals("1")) {
    lcd1.clear();
    lcd1.setCursor(0, 0);
    lcd1.print("Commanded Speed:");
    lcd1.setCursor(0, 1);
    lcd1.print(incomingData.substring(5, incomingData.length()));
  }

  if (incomingData.substring(2, 3).equals("1")) {
    lcd1.clear();
    lcd1.setCursor(0, 0);
    lcd1.print("Switch: " + incomingData.substring(5, incomingData.length()));

  }

  if (incomingData.substring(3, 4).equals("1")) {
    lcd1.clear();
    lcd1.setCursor(0, 0);
    lcd1.print("Light:");
    lcd1.setCursor(0, 1);
    lcd1.print(incomingData.substring(5, incomingData.length()));
    if (incomingData.substring(4, 5).equals("0")) {
      digitalWrite(Red_LED, HIGH);
    } else if (incomingData.substring(4, 5).equals("1")) {
      digitalWrite(Red_LED, HIGH);
      digitalWrite(Green_LED, HIGH);
    } else if (incomingData.substring(4, 5).equals("2")) {
      digitalWrite(Red_LED, HIGH);
      digitalWrite(Green_LED, HIGH);
      digitalWrite(Super_Green, HIGH);
    }
  }
  */
}

void setup() {
  Serial.begin(9600);
  pinMode(2, OUTPUT);
  pinMode(3, OUTPUT);
  pinMode(4, OUTPUT);
  pinMode(5, OUTPUT);

  Light lights[LIGHTNUMBER];
  Switch switches[SWITCHNUMBER];
  lights[0].name = 
}


void loop() {
  lcd1.init();
  lcd1.backlight();
  Receiver();
  delay(500);
