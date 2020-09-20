// Forked from -> www.elegoo.com 's RGB LED tutorial
// https://www.meccanismocomplesso.org/en/tutorial-sending-values-from-pc-to-arduino-by-serial-communication/

// define pins
#define BLUE_Weather 9
#define GREEN_Weather 10
#define RED_Weather 11

#define BLUE_Email 3
#define GREEN_Email 5
#define RED_Email 6

#define RED_Class 13
void setup()
{
  Serial.begin(9600);

  pinMode(RED_Class, OUTPUT);
  
  pinMode(RED_Weather, OUTPUT);
  pinMode(GREEN_Weather, OUTPUT);
  pinMode(BLUE_Weather, OUTPUT);

  pinMode(RED_Email, OUTPUT);
  pinMode(GREEN_Email, OUTPUT);
  pinMode(BLUE_Email, OUTPUT);
  
  digitalWrite(RED_Class, HIGH);
  //digitalWrite(GREEN, LOW);
  //digitalWrite(BLUE, LOW);
}

// define variables
int redValue;
int greenValue;
int blueValue;

int Stage = 0;

void CheckForErrorFromPc(char c){
    if(c == 126){

    analogWrite(RED_Email, 0);
    analogWrite(GREEN_Email, 0);
    analogWrite(BLUE_Email, 0);
    
    analogWrite(RED_Weather, 0);
    analogWrite(GREEN_Weather, 0);
    analogWrite(BLUE_Weather, 0);

    digitalWrite(RED_Class, LOW);
    Serial.end();
    exit(1);
  }
}
void RecieveData(char * arr){
  // Weather Percent Data
  char ch;
  if(Stage == 0){
    ch = Serial.read();
    CheckForErrorFromPc(ch);
    arr[0] = ch;
    Stage++;
    return;
  }else if(Stage == 1){
  // Email int data
  ch = Serial.read();
  CheckForErrorFromPc(ch);
  arr[1] = ch;
  Stage++;
  return;
  }else if(Stage == 2){
    // Class int data
    ch = Serial.read();
    CheckForErrorFromPc(ch);
    arr[2] = ch;
    Stage++;
    return;
  }

    
}

void TurnOnLights(char * arr){
  // The Raspberry PI has run into a fatal error and wants you to die with it :)

  // Weather Percent
  if(arr[0]== 49){
    redValue = 255;
    greenValue = 0;
    blueValue = 0;
  }else{
    redValue = 0;
    greenValue = 255;
    blueValue = 0;
  }
  analogWrite(RED_Weather, redValue);
  analogWrite(GREEN_Weather, greenValue);
  analogWrite(BLUE_Weather, blueValue);

  if(arr[1] == 48){
    redValue = 0;
    greenValue = 255;
    blueValue = 0;
  }else if(arr[1] == 49){
    redValue = 100;
    greenValue = 100;
    blueValue = 0;
  }else if(arr[1] == 50){
    redValue = 100;
    greenValue = 0;
    blueValue = 100;
  }else if(arr[1] == 51){
    redValue = 255;
    greenValue = 0;
    blueValue = 0;
  }else{
    redValue = 100;
    greenValue = 100;
    blueValue = 100;
  }
  analogWrite(RED_Email, redValue);
  analogWrite(GREEN_Email, greenValue);
  analogWrite(BLUE_Email, blueValue);

  if(arr[2] == 49){
    digitalWrite(RED_Class, HIGH);
  }else if(arr[2] == 48){
    digitalWrite(RED_Class, LOW);
  }
  
}


// main loop
void loop()
{

  /*
  redValue = 0;
  greenValue = 255;
  blueValue = 0;
  digitalWrite(
  analogWrite(RED_Weather, redValue);
  analogWrite(GREEN_Weather, greenValue);
  analogWrite(BLUE_Weather, redValue);
  analogWrite(RED_Email, redValue);
  analogWrite(GREEN_Email, greenValue);
  analogWrite(BLUE_Email, redValue);
  
  delay();
  */
  
}

char DataArray[3];
void serialEvent()
{
   while(Serial.available()) 
   {
      RecieveData(DataArray);
      if(Stage == 3){
        TurnOnLights(DataArray);
        Stage = 0;
      }
    
   }
}
