// Include library code
#include <Wire.h>
#include <LiquidCrystal_I2C.h>

LiquidCrystal_I2C lcd1(0x20, 20, 4);
String incomingData;

int green[150] = {0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0};

//String commanded[150];


int blue[13] = {0,0,0,0,0,0,0,0,0,0,0,0,0};

String current_block = "F28";


const int LIGHTNUMBER = 4;
const int SWITCHNUMBER = 3;

char flogic[50];
char dlogic[50];
char ilogic[50];
int Fsize = 0;
int Dsize = 0;
int Isize = 0;


bool manual = true;
bool switch_change = true;
bool light_change = true;

bool FED = false;
bool ABC = false;
bool ZYX = false;

String boolean_logic = "DFAZ0 EFAZ1";


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

bool deMorg(bool value, bool value2, String operation){
  bool compare1;
  bool compare2;
  if(operation = "and"){
    compare1 = !(value && value2);
    compare2 = !value || !value2;
    if(compare1 == compare2){
      return true;
    }
  }
  else{
    compare1 = !(value || value2);
    compare2 = !value && !value2;
    if(compare1 == compare2){
      return true;
    }   
  }
  return false;
}

bool parsePLC(char logic){
  if(logic == 'F'){
    return FED;
  }
  else if(logic == 'A'){
    return ABC;
  }
  else if(logic == 'Z'){
    return ZYX;
  }
  else if(logic == 'f'){
    return !FED;
  }
  else if(logic == 'a'){
    return !ABC;
  }
  else if(logic == 'z'){
    return !ZYX;
  }
  else{
    return false;
  }
}

void PLC(){
  int prev_value = 0;
  int index = 0;
  bool light_switch = false;
  for(int i = 0; i < SWITCHNUMBER; i++){
    if(current_block == switches[i].name){
      prev_value = switches[i].value;
      index = i;
      light_switch = false;
    }
  }
  for(int i = 0; i < LIGHTNUMBER; i++){
    if(current_block == lights[i].name){
      prev_value = lights[i].value;
      index = i;
      light_switch = true;
    }  
  }

  int indexF = Fsize;
  int for_and = 0;
  bool resultF;
  if(flogic[indexF-1] == '0'){
    for_and = 0;
  }
  else if(flogic[indexF-1] == '1'){
    for_and = 1;
  }
  indexF--;
  resultF = parsePLC(flogic[indexF-1]);
  indexF--;
  while(indexF > 0){
    char logic = flogic[indexF-1];
    if(for_and == 0){
      if(deMorg(resultF, parsePLC(logic), "or")){
        resultF = resultF || parsePLC(logic);
      } 
    }
    else if(for_and == 1){
      if(deMorg(resultF, parsePLC(logic), "and")){
        resultF = resultF && parsePLC(logic);
      }
    }
    indexF--;
  }
  switches[1].value = resultF;
  if(resultF == 0){
    lights[2].value = 0;
    lights[3].value = 1;
  }
  else{
    lights[2].value = 1;
    lights[3].value = 0;
  }
  Serial.print("F28/"+ String(switches[1].value) + " G29/" + String(lights[2].value) + " Z150/" + String(lights[3].value) + "\n");

  int indexD = Dsize;
  int dor_and = 0;
  bool resultD;
  if(dlogic[indexD-1] == '0'){
    dor_and = 0;
  }
  else if(dlogic[indexD-1] == '1'){
    dor_and = 1;
  }
  indexD--;
  resultD = parsePLC(dlogic[indexD-1]);
  indexD--;
  while(indexD > 0){
    char logic = dlogic[indexD-1];
    if(dor_and == 0){
      if(deMorg(resultD, parsePLC(logic), "or")){
        resultD = resultD || parsePLC(logic);
      }
    }
    else if(dor_and == 1){
      if(deMorg(resultD, parsePLC(logic), "and")){
        resultD = resultD && parsePLC(logic);
      }
    }
    indexD--;
  }
  switches[0].value = resultD;
  if(resultD == 0){
    lights[0].value = 1;
    lights[1].value = 0;
  }
  else{
    lights[0].value = 0;
    lights[1].value = 1;
  }
  Serial.print("D13/"+ String(switches[0].value) + " A1/" + String(lights[0].value) + " C12/" + String(lights[1].value) + "\n");

  int indexI = Isize;
  int ior_and = 0;
  bool resultI;
  if(ilogic[indexI-1] == '0'){
    ior_and = 0;
  }
  else if(ilogic[indexI-1] == '1'){
    ior_and = 1;
  }
  indexI--;
  resultI = parsePLC(ilogic[indexI-1]);
  indexI--;
  while(indexI > 0){
    char logic = ilogic[indexI-1];
    if(ior_and == 0){
      if(deMorg(resultI, parsePLC(logic), "or")){
        resultI = resultI || parsePLC(logic);
      }
    }
    else if(ior_and == 1){
      if(deMorg(resultI, parsePLC(logic), "and")){
        resultI = resultI && parsePLC(logic);
      }
    }
    indexI--;
  }
  switches[2].value = resultI;
  Serial.print("I57/"+ String(switches[2].value)+ "\n");

  if(light_switch){
    if(lights[index].name == current_block){
      if(lights[index].value != prev_value){
        display_block(current_block);
      }
    }
  }
  else if(!light_switch){
    if(switches[index].name == current_block){
      if(switches[index].value != prev_value){
        display_block(current_block);
      }
    }
  }
}

void populateLogic(String expression) {
  // Default result if expression is not recognized
  // Iterate through the characters in the expression
  
  int index = 0;
  int switch_type = -1;
  while(expression.length() > index){
    char currentChar = expression.charAt(index);
    if(index == 0){
      if(currentChar == 'D'){
        switch_type = 0;
        Dsize = 0;
      }
      else if(currentChar == 'E'){
        switch_type = 1;
        Fsize = 0;
      }
      else if(currentChar == 'J'){
        switch_type = 2;
        Isize = 0;
      }
    }
    else{
      if(switch_type == 0){
        dlogic[Dsize] = currentChar;
        Dsize++;
      }
      else if(switch_type == 1){
        flogic[Fsize] = currentChar;
        Fsize++;
      }
      else if(switch_type == 2){
        ilogic[Isize] = currentChar;
        Isize++;
      }
    }
    index++;
  }  
}


void PLCSplit(String incoming) {
  // Split the string by space
  int spaceIndex = incoming.indexOf(' ');

  while (spaceIndex != -1) {
    // Find the position of the first space
    spaceIndex = incoming.indexOf(' ');

    // Extract the substring before the space
    String token = incoming.substring(0, spaceIndex);

    populateLogic(token);
    // Remove the processed part (including the space)
    incoming = incoming.substring(spaceIndex + 1);

    // Find the position of the next space
    spaceIndex = incoming.indexOf(' ');
  }
  
  populateLogic(incoming);
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
  }
  else if(detect.equals("1")){
    boolean_logic = incomingData.substring(1,incomingData.length());
    PLCSplit(boolean_logic);
  }

  //read the block occupancy -- PLC
  else if(detect.equals("2")){
    for(int i = 0; i < 150; i++){
      green[i] = 0;
    }
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
  lcd1.setCursor(0,1);
  lcd1.print(String(incomingData));
  incomingData = "";
}

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
    lcd1.setCursor(0,0);
    PLC();
  }
  delay(500);

  //transmit(); 
}
