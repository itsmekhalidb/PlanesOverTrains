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


String current_block = "F28";


const int LIGHTNUMBER = 4;
const int SWITCHNUMBER = 3;

char flogic[50];
char dlogic[50];
char ilogic[50];
int fsize = 0;
int dsize = 0;
int isize = 0;


bool manual = true;
bool switch_change = true;
bool light_change = true;

bool fed_section = false;
bool abc_section = false;
bool zyx_section = false;
bool i_section = false;

String boolean_logic = "";


int Detect_LED = 2;
int Red_LED = 3;
int green_LED = 4;
int Crossing_LED = 5;


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

void update_blocks(){
  bool zyx_temp = false;
  bool abc_temp = false;
  bool fed_temp = false;
  bool i_temp = false;
  for(int i = 144; i < 150; i++){
    zyx_temp = zyx_temp || bool(green[i]);
  }
  for(int i = 0; i < 12; i++){
    abc_temp = abc_temp || bool(green[i]);
  }
  for(int i = 12; i < 28; i++){
    fed_temp = fed_temp || bool(green[i]);
  }
  for(int i =40; i < 57; i++){
    i_temp = i_temp || bool(green[i]);
  }
  fed_section = fed_temp;
  abc_section = abc_temp;
  zyx_section = zyx_temp;
  i_section = i_temp;
}

bool demorgan_law(bool value, bool value2, String operation){
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

bool parse_plc(char logic){
  if(logic == 'F'){
    return fed_section;
  }
  else if(logic == 'A'){
    return abc_section;
  }
  else if(logic == 'Z'){
    return zyx_section;
  }
  else if(logic == 'I'){
    return i_section;
  }
  else if(logic == 'f'){
    return !fed_section;
  }
  else if(logic == 'a'){
    return !abc_section;
  }
  else if(logic == 'z'){
    return !zyx_section;
  }
  else if(logic == 'i'){
    return !i_section;
  }
  else{
    return false;
  }
}

void plc(){
  int prev_value_switch = 0;
  int prev_value_light = 0;
  int light_index = 0;
  int switch_index = 0;
  bool light_here = false;
  bool switch_here = false;
  for(int i = 0; i < SWITCHNUMBER; i++){
    if(current_block == switches[i].name){
      prev_value_switch = switches[i].value;
      switch_index = i;
      switch_here= true;
    }
  }
  for(int i = 0; i < LIGHTNUMBER; i++){
    if(current_block == lights[i].name){
      prev_value_light = lights[i].value;
      light_index = i;
      light_here = true;
    }  
  }

  int index_f = fsize;
  int for_and = 0;
  bool result_f;
  if(flogic[index_f-1] == '0'){
    for_and = 0;
  }
  else if(flogic[index_f-1] == '1'){
    for_and = 1;
  }
  index_f--;
  result_f = parse_plc(flogic[index_f-1]);
  index_f--;
  while(index_f > 0){
    char logic = flogic[index_f-1];
    if(for_and == 0){
      if(demorgan_law(result_f, parse_plc(logic), "or")){
        result_f = result_f || parse_plc(logic);
      } 
    }
    else if(for_and == 1){
      if(demorgan_law(result_f, parse_plc(logic), "and")){
        result_f = result_f && parse_plc(logic);
      }
    }
    index_f--;
  }
  switches[1].value = result_f;
  if(result_f == 0){
    lights[2].value = 0;
    lights[3].value = 1;
  }
  else{
    lights[2].value = 1;
    lights[3].value = 0;
  }
  Serial.print("0F28/"+ String(switches[1].value) + " 1F28/" + String(lights[2].value) + " 1Z150/" + String(lights[3].value) + "\n");

  int index_d = dsize;
  int dor_and = 0;
  bool result_d;
  if(dlogic[index_d-1] == '0'){
    dor_and = 0;
  }
  else if(dlogic[index_d-1] == '1'){
    dor_and = 1;
  }
  index_d--;
  result_d = parse_plc(dlogic[index_d-1]);
  index_d--;
  while(index_d > 0){
    char logic = dlogic[index_d-1];
    if(dor_and == 0){
      if(demorgan_law(result_d, parse_plc(logic), "or")){
        result_d = result_d || parse_plc(logic);
      }
    }
    else if(dor_and == 1){
      if(demorgan_law(result_d, parse_plc(logic), "and")){
        result_d = result_d && parse_plc(logic);
      }
    }
    index_d--;
  }
  switches[0].value = result_d;
  if(result_d == 0){
    lights[0].value = 1;
    lights[1].value = 0;
  }
  else{
    lights[0].value = 0;
    lights[1].value = 1;
  }
  Serial.print("0D13/"+ String(switches[0].value) + " 1A1/" + String(lights[0].value) + " 1D13/" + String(lights[1].value) + "\n");

  int index_i = isize;
  int ior_and = 0;
  bool result_i;
  if(ilogic[index_i-1] == '0'){
    ior_and = 0;
  }
  else if(ilogic[index_i-1] == '1'){
    ior_and = 1;
  }
  index_i--;
  result_i = parse_plc(ilogic[index_i-1]);
  index_i--;
  while(index_i > 0){
    char logic = ilogic[index_i-1];
    if(ior_and == 0){
      if(demorgan_law(result_i, parse_plc(logic), "or")){
        result_i = result_i || parse_plc(logic);
      }
    }
    else if(ior_and == 1){
      if(demorgan_law(result_i, parse_plc(logic), "and")){
        result_i = result_i && parse_plc(logic);
      }
    }
    index_i--;
  }
  switches[2].value = result_i;
  Serial.print("0I57/"+ String(switches[2].value)+ "\n");

  if(light_here && switch_here){
    if(lights[light_index].name == current_block && switches[switch_index].name == current_block){
      if(lights[light_index].value != prev_value_light || switches[switch_index].value != prev_value_switch){
        display_block(current_block);
      }
    }
  }
  else if(light_here){
    if(lights[light_index].name == current_block){
      if(lights[light_index].value != prev_value_light){
        display_block(current_block);
      }
    }
  }
  else if(switch_here){
    if(switches[switch_index].name == current_block){
      if(switches[switch_index].value != prev_value_switch){
        display_block(current_block);
      }
    }
  }
}

void populate_logic(String expression) {
  // Default result if expression is not recognized
  // Iterate through the characters in the expression
  
  int index = 0;
  int switch_type = -1;
  while(expression.length() > index){
    char currentChar = expression.charAt(index);
    if(index == 0){
      if(currentChar == 'D'){
        switch_type = 0;
        dsize = 0;
      }
      else if(currentChar == 'E'){
        switch_type = 1;
        fsize = 0;
      }
      else if(currentChar == 'J'){
        switch_type = 2;
        isize = 0;
      }
    }
    else{
      if(switch_type == 0){
        dlogic[dsize] = currentChar;
        dsize++;
      }
      else if(switch_type == 1){
        flogic[fsize] = currentChar;
        fsize++;
      }
      else if(switch_type == 2){
        ilogic[isize] = currentChar;
        isize++;
      }
    }
    index++;
  }  
}


void plc_split(String incoming) {
  // Split the string by space
  int space_index = incoming.indexOf(' ');

  while (space_index != -1) {
    // Find the position of the first space
    space_index = incoming.indexOf(' ');

    // Extract the substring before the space
    String token = incoming.substring(0, space_index);

    populate_logic(token);
    // Remove the processed part (including the space)
    incoming = incoming.substring(space_index + 1);

    // Find the position of the next space
    space_index = incoming.indexOf(' ');
  }
  
  populate_logic(incoming);
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


void receiver(){
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
    plc_split(boolean_logic);
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
  }
  //lcd1.setCursor(0,1);
  //lcd1.print(String(incomingData));
  incomingData = "";
}

void auto_manual(){
  int reading = digitalRead(6);
  if (reading == 0) {
    manual = !manual;
  }
}

void change_switch(){
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
        Serial.print("0" + current_block + "/"+ String(switches[i].value));
        break;
      }
    }
  }
}

void change_light(){
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
        Serial.print("1" + current_block + "/"+ String(lights[i].value));
        break;
      }
    }
  }
}

void crossing_lights(){
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
  lights[1].name = "D13";
  lights[1].value = 0;
  lights[2].name = "F28";
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
  
  receiver();
  update_blocks();
  crossing_lights();
  auto_manual(); 
  if(!manual){
    change_switch();
    change_light();
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
    plc();
  }
  delay(500);

}
