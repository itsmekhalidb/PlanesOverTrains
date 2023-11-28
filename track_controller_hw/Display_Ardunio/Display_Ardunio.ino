// Include library code
#include <Wire.h>
#include <LiquidCrystal_I2C.h>
#include <map>
#include <vector>

LiquidCrystal_I2C lcd1(0x20, 20, 4);
String incomingData;

int green[150] = {0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0};

//String commanded[150];


int blue[13] = {0,0,0,0,0,0,0,0,0,0,0,0,0};

String current_block = "F28";


const int LIGHTNUMBER = 4;
const int SWITCHNUMBER = 3;


bool manual = true;
bool switch_change = true;
bool light_change = true;

bool FED = false;
bool ABC = false;
bool ZYX = false;

int switch_d13_logic[32];
int switch_f28_logic[32];
int light_a1_logic[2];
int light_c12_logic[2];
int light

int Detect_LED = 2;
int Red_LED = 3;
int green_LED = 4;
int Crossing_LED = 5;

struct Block{
  String name;
  int occupancy;
  int commanded;
};

struct Light{
  String name;
  int value;
};

struct Switch{
  String name;
  int value;
};

Light lights[LIGHTNUMBER];
Switch switches[SWITCHNUMBER];

void transmit(){
  Serial.print("Hello");
}

void update_blocks(){
  for(int i = 144; i < 150; i++){
    ZYX = ZYX || bool(green[i]);
  }
  for(int i = 0; i < 12; i++){
    ABC = ABC || bool(green[i]);
  }
  for(int i = 12; i < 28; i++){
    FED = FED || bool(green[i]);
  }

}
/*
String Structure by Index

First two tokens 
***************************
First = FED, Second = ABC, Third = ZYX, Fourth = Switch D13 or Switch F28

Remaining Tokens 
***************************
First = Switch D13 or Switch F28, Second = Light A1 or C12 or Light G29 or Z150
*/

void PLC(String incomingData){

  String values[6];
  int tokenCount = 0;
    // Split the string by space
  while (incomingData.length() > 0 && tokenCount < 6) {
    // Find the position of the first space
    int spaceIndex = incomingData.indexOf(' ');
    
    // Extract the substring before the space
    String token = incomingData.substring(0, spaceIndex);
    
    // Add the token to the array
    values[tokenCount++] = token;
    
    // Remove the processed part (including the space)
    incomingData = incomingData.substring(spaceIndex + 1);
  }
  for(int i = 0; i < values[0].length(); i++){
    String value = values[0].substring(i,i+1);

  }
  

}

void display_block(String block_number){
  lcd1.clear();
  digitalWrite(Red_LED, LOW);
  digitalWrite(green_LED, LOW);
  lcd1.setCursor(0,0);
  lcd1.print("Block #: " + block_number);
  lcd1.setCursor(0,1);
    //lcd1.print("Commanded Speed: " + commanded[atoi(block_number)]);
  for(int i = 0; i < LIGHTNUMBER; i++){
    if(lights[i].name == block_number){
      if(lights[i].value == 1){
        digitalWrite(Red_LED, HIGH);
        digitalWrite(green_LED, HIGH);
      }
      else if(lights[i].value == 0){
        digitalWrite(Red_LED, HIGH);
        digitalWrite(green_LED, LOW);
      }
        break;
    }
    else{
        digitalWrite(Red_LED, LOW);
        digitalWrite(green_LED, LOW);
    }
  }
  for(int i = 0; i < SWITCHNUMBER; i++){
    if(switches[i].name == block_number){
      lcd1.setCursor(0,2);
      if(switches[i].value == 0){
        lcd1.print("Switch: Right");
      }
      else if(switches[i].value == 1){
        lcd1.print("Switch: Left");
      }
      break;
    }
  }
}


void Receiver(){
  if (Serial.available() > 0) {
    incomingData = Serial.readStringUntil('\n');
  }
  
  String detect = incomingData.substring(0,1);

//display each block
  if(detect.equals("0")){
    current_block = incomingData.substring(1,incomingData.length());
    display_block(current_block);
    lcd1.setCursor(0,1);
    lcd1.print("Block");
  }

  //read the block occupancy -- PLC
  else if(detect.equals("2")){
    for(int i = 0; i < 150; i++){
      green[i] = 0;
    }
    lcd1.setCursor(0,1);
    lcd1.print(String(incomingData));
    String occupancy = incomingData.substring(2, incomingData.length());
   // lcd1.print(occupancy.length());
    while(occupancy.length() > 0){  
      int space = occupancy.indexOf(" ");
      if(space == -1){
        int num = occupancy.substring(0, occupancy.length()).toInt();
        //if(current_block.substring(1, current_block.length()).equals(occupancy.substring(0, occupancy.length()))){
        //  display_block(current_block);
        //}
        //lcd1.setCursor(0,1);
        //lcd1.print(String(num));
        green[num-1] = 1;
        break;
      }
      int num = occupancy.substring(0, space).toInt();
      green[num-1] = 1;
      //if(current_block.substring(1, current_block.length()).equals(occupancy.substring(0, space))){
      //  display_block(current_block);
      //}
      occupancy = occupancy.substring(space + 1);     
    }
   // display_block(current_block);
   // lcd1.setCursor(0,2);
   // lcd1.print(String(green[76]));
  }
  incomingData = "";

void autoManual(){
  int reading = digitalRead(6);
  if (reading == 0) {
    manual = !manual;
  }
}

void changeSwitch(){
  int reading = digitalRead(7);
  if (reading == 0){
    for(int i = 0; i < SWITCHNUMBER; i++){
      if(switches[i].name == current_block){
        if(switches[i].value == 0){
          switches[i].value = 1;
              lcd1.setCursor(0,2);
              lcd1.print("               ");
              lcd1.setCursor(0,2);
              lcd1.print("Switch: Left");
        }
        else{
          switches[i].value = 0;
              lcd1.setCursor(0,2);
              lcd1.print("                ");
              lcd1.setCursor(0,2);
              lcd1.print("Switch: Right");
        }
        Serial.print(current_block + "/"+ String(switches[i].value));
        break;
      }
    }
  }
}

void changeLight(){
  int reading = digitalRead(8);
  if (reading == 0) {
    for(int i = 0; i < LIGHTNUMBER; i++){
      if(lights[i].name == current_block){
        if(lights[i].value == 0){
          lights[i].value = 1;
          digitalWrite(Red_LED, HIGH);
          digitalWrite(green_LED, HIGH);
        }
        else{
          lights[i].value = 0;   
          digitalWrite(Red_LED, HIGH);
          digitalWrite(green_LED, LOW);  
        }
        Serial.print(current_block + "/"+ String(lights[i].value));
        break;
      }
    }
  }
}

void crossingLights(){
  if(green[18] == 1){
    digitalWrite(Crossing_LED, HIGH);
  }
  else{
    digitalWrite(Crossing_LED, LOW);
  }
}


    

void setup() {
  Serial.begin(9600);
  lcd1.init();
  lcd1.backlight();
  pinMode(2, OUTPUT);
  pinMode(3, OUTPUT);
  pinMode(4, OUTPUT);
  pinMode(5, OUTPUT);
  pinMode(6, INPUT_PULLUP);
  pinMode(7, INPUT_PULLUP);
  pinMode(8, INPUT_PULLUP);

 // for (int i = 0; i < 13; i++) {
  //  commanded[i] = "0"; // Initialize each string as empty
  //}

  lights[0].name = "A1";
  lights[0].value = 1;
  lights[1].name = "C12";
  lights[1].value = 0;
  lights[2].name = "G29";
  lights[2].value = 0;
  lights[3].name = "Z150";
  lights[3].value = 1;
  switches[0].name = "D13";
  switches[0].value = 0;
  switches[1].name = "F28";
  switches[1].value = 1;
  switches[2].name = "I57";
  switches[2].value = 0;

  display_block(current_block);
}

void loop() {
  /*
  Receiver();
  if(manual){
    PLC();
  }
  */
  Receiver();
  update_blocks();
  crossingLights();
  autoManual();
  if(!manual){
    changeSwitch();
    changeLight();
    lcd1.setCursor(0,3);
    lcd1.print("      ");
    lcd1.setCursor(0,3);
    lcd1.print("Manual");
  }
  else{
    lcd1.setCursor(0,3);
    lcd1.print("      ");
    lcd1.setCursor(0,3);
    lcd1.print("Auto");
   // PLC();
  }
  delay(100);

  //transmit(); 
}
