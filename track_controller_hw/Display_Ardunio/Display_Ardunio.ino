// Include library code
#include <Wire.h>
#include <LiquidCrystal_I2C.h>

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

String current_block = "M76";


const int LIGHTNUMBER = 4;
const int SWITCHNUMBER = 2;

bool manual = true;

int Detect_LED = 2;
int Red_LED = 3;
int Green_LED = 4;
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

void PLC(){
  bool sectM = bool(green[75]) || bool(green[62]);
  bool sectN = bool(green[76]) || bool(green[84]);
  bool sectQO = bool(green[85]) || bool(green[99]);
  if((!sectM && !sectN && sectQO) || (sectM && !sectN && sectQO) || (!sectM && sectN && sectQO)){
    switches[0].value = 1;
    switches[1].value = 0;
    lights[0].value = 0;
    lights[1].value = 1;
    lights[2].value = 1;
    lights[3].value = 0;
    Serial.print("100110");
  }
  else if((!sectM && sectN && !sectQO) || (sectM && sectN && sectQO)){
    switches[0].value = 1;
    switches[1].value = 1;
    lights[0].value = 0;
    lights[1].value = 1;
    lights[2].value = 0;
    lights[3].value = 1;
    Serial.print("110101"); 
  }
  else if((sectM && !sectN && !sectQO) || (sectM && sectN && !sectQO) || (!sectM && !sectN && !sectQO)){
    switches[0].value = 0;
    switches[1].value = 1;
    lights[0].value = 1;
    lights[1].value = 0;
    lights[2].value = 0;
    lights[3].value = 1;
    Serial.print("011001");
  }
}

void display_block(String block_number){
  lcd1.setCursor(0,0);
  lcd1.print("Block #: " + block_number);
  lcd1.setCursor(0,1);
    //lcd1.print("Commanded Speed: " + commanded[atoi(block_number)]);
  for(int i = 0; i < LIGHTNUMBER; i++){
    if(lights[i].name == block_number){
      if(lights[i].value == 1){
        digitalWrite(Red_LED, HIGH);
        digitalWrite(Green_LED, HIGH);
      }
      else if(lights[i].value == 0){
        digitalWrite(Red_LED, HIGH);
        digitalWrite(Green_LED, LOW);         
      }
        break;
    }
    else{
        digitalWrite(Red_LED, LOW);
        digitalWrite(Green_LED, LOW); 
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
  /*
  lcd1.setCursor(0,3);
  lcd1.print(incomingData);
  */
  
// toggle a light or switch - manual mode
  if (detect.equals("1")) {
    digitalWrite(Detect_LED, HIGH);
    digitalWrite(Red_LED, LOW);
    digitalWrite(Green_LED, LOW);
    digitalWrite(Crossing_LED, LOW);
    String commanded_speed = incomingData.substring(1,3);
    String light_is = incomingData.substring(3,4);
    String light_state = incomingData.substring(4,5);
    String switch_is = incomingData.substring(5,6);
    String switch_state = incomingData.substring(6,7);
    String crossing_is = incomingData.substring(7,8);
    String crossing_state = incomingData.substring(8,9);
    String block_number = incomingData.substring(9,incomingData.length());
    
  
    //lcd1.clear();
    //lcd1.setCursor(0, 0);
    //lcd1.print("Block #: " + block_number);
    //lcd1.setCursor(0, 1);
    //lcd1.print("Commanded Speed: " + commanded_speed);

    //commanded[atoi(number_of_block)] = atoi(commanded_speed);

    if(light_is == "1"){
      for(int i = 0; i < LIGHTNUMBER; i++){
        if(lights[i].name == block_number){
          if(light_state == "0"){
            lights[i].value = 0;
          }
          else{
            lights[i].value = 1;
          }
          break;
        }
      }
    }
    if(switch_is == "1"){
      for(int i = 0; i < SWITCHNUMBER; i++){
        if(switches[i].name == block_number){
          if(switch_state == "0"){
            switches[i].value = 0;
          }
          else{
            switches[i].value = 1;
          }
          break;
        }
      }
    }
  }
//display each block
  else if (detect.equals("0")){
    current_block = incomingData.substring(1,incomingData.length());
    display_block(current_block);
  }

  //read the block occupancy -- PLC
  else if(detect.equals("2")){
    for(int i = 0; i < 150; i++){
      green[i] = 0;
    }
    String occupancy = incomingData.substring(2, incomingData.length());
    lcd1.print(occupancy.length());
    while(occupancy.length() > 0){  
      int space = occupancy.indexOf(" ");
      if(space == -1){
        int num = occupancy.substring(0, occupancy.length()).toInt();
        if(current_block.substring(1, current_block.length()).equals(occupancy.substring(0, occupancy.length()))){
          display_block(current_block);
        }
        lcd1.setCursor(0,1);
        lcd1.print(String(num));
        green[num-1] = 1;
        break;
      }
      int num = occupancy.substring(0, space).toInt();
      green[num-1] = 1;
      if(current_block.substring(1, current_block.length()).equals(occupancy.substring(0, space))){
        display_block(current_block);
      }
      occupancy = occupancy.substring(space + 1);     
    }
    lcd1.setCursor(0,2);
    lcd1.print(String(green[76]));
  }

  else if(detect.equals("3")){
    manual = false;
    display_block(current_block);
  }

  else if(detect.equals("4")){
    manual = true;
    display_block(current_block);
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


void setup() {
  Serial.begin(9600);
  pinMode(2, OUTPUT);
  pinMode(3, OUTPUT);
  pinMode(4, OUTPUT);
  pinMode(5, OUTPUT);

 // for (int i = 0; i < 13; i++) {
  //  commanded[i] = "0"; // Initialize each string as empty
  //}

  lights[0].name = "M76";
  lights[0].value = 0;
  lights[1].name = "R101";
  lights[1].value = 0;
  lights[2].name = "Q100";
  lights[2].value = 0;
  lights[3].name = "N85";
  lights[3].value = 0;
  switches[0].name = "M76";
  switches[0].value = 0;
  switches[1].name = "N85";
  switches[1].value = 0;
}


void loop() {
  lcd1.init();
  lcd1.backlight();
  Receiver();
  if(manual){
    PLC();
  }
  //transmit();
  
}
