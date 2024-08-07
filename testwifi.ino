#include <SoftwareSerial.h>

SoftwareSerial espSerial(2,3);

int blindDown = 13;
int blindUpp = 14;

int endDown = 15;
int endUpp = 16;

#define ssid "kedem"
#define PASSWORD "noamalmamilo"

String fmsg;
String cmd;

void setup() 
{
  espSerial.begin(9600);
  Serial.begin(9600);
  espSetup();
}

void loop() 
{ 
  String msg;
  
  while(espSerial.available()){
      fmsg += (char)espSerial.read();
      delay(2);   
  }
   
  msg = getString(fmsg);
  
  if(msg != NULL){
    Serial.println(msg);
    if (msg == "blindDown") {
        digitalWrite(blindUpp, LOW);
        delay(10);
        digitialWrite(blindDown, HIGH);
    }
    if (msg == "blindUpp") {
        digitalWrite(blindDown, LOW);
            delay(10);
        digitialWrite(blindUpp, HIGH);
    }
    if (msg == "blindStop") {
        digitalWrite(blindUpp, LOW)
        digitialWrite(blindDown, LOW);
    }
    delay(250);
  }

  if(digitalRead(endDown) == HIGH) {
      digitalWrite(blindDown, LOW);
  }
  if (digitalRead(endUpp) == HIGH) {
      digitalWrite(blindUpp, LOW);
  }
}


void espSetup()
{
    int counter=0;
    Serial.println("-----------Setup Begin------------");
    
    // Step 1 Reset ESP8266
    espSerial.println("AT+RST");
    delay(2000);
    getResponse();
    
    // Step 2 Connection Test of ESP8266
    Serial.println("-------------TEST AT----------");
    while(1){
       espSerial.println("AT");
       delay(250);
       if(espSerial.find("OK")){
        counter+=1;
        } 
       if(counter == 10){
        Serial.println("Test OK");
        counter=0;
        break;
        }
       else{
        Serial.println("Waiting...");
        }
      }

    // Step 3 Station Mode
    Serial.println("-------------STATION MODE----------");
    while(1){
      espSerial.println("AT+CWMODE=1");
      delay(250);
      if(espSerial.find("OK")){
        counter+=1;
        }
      if(counter == 10){
        Serial.println("Station Mode Setted 1");
        counter=0;
        break;
        }
      else{
        Serial.println("Waiting...");
        }
      }
    
    // Step 4 Connect to WiFi
    Serial.println("-------------CONNECT TO WIFI----------");
    while(1){
      cmd = "AT+CWJAP=\"";
      cmd += ssid;
      cmd += "\",\"";
      cmd += PASSWORD;
      cmd += "\"";
      espSerial.println(cmd);
      if(espSerial.find("OK")){
        counter+=1;
        }
      if(counter == 3){
        Serial.println("Connection Established");
        counter=0;
        break;
        }
      else{
        Serial.println("Waiting...");
        }
      }
      
    // Step 5 Find IP Address
    Serial.println("-------------FIND IP----------");
    espSerial.println("AT+CIFSR");
    delay(2000);
    getResponse();

    // Step 6 Setting Multiple Connections
    Serial.println("-------------SET MULTIPLE CONNECTIONS----------");
    while(1){
      espSerial.println("AT+CIPMUX=1");
      delay(250);
      if(espSerial.find("OK")){
        counter+=1;
        }
      if(counter == 10){
        Serial.println("Multiple Connections Enabled");
        counter = 0;
        break;
        }
      else{
        Serial.println("Waiting...");
        }
      }

    // Step 7 Setting Port 8080
    Serial.println("-------------SET PORT 8080----------");
    while(1){
     espSerial.println("AT+CIPSERVER=1,8080");
     delay(500);
     if(espSerial.find("OK")){
       counter+=1;
       }
     if(counter == 10){
       Serial.println("Setting Port 8080");
       counter = 0;
       break;
       }
     else{
       Serial.println("Waiting...");
       }
     }

    Serial.println("---------SETUP DONE--------");
    delay(250);
}


void getResponse()
{
  String response;
  
  while(espSerial.available()){
      char c = espSerial.read();
      response += c;
      }
  Serial.println(response);
}


String getString(String flmsg)
{ 
  int lng = 0,delimiter = 0;
  String lmsg;
  
  lng = flmsg.length();  
  for(int i=0;i<lng;i++){
     if(flmsg[i] == ':'){
      delimiter = i;
      }
     if(i > delimiter && delimiter != 0){
      lmsg += flmsg[i];
      }
    }
  fmsg = ""; 
  return lmsg;
}
