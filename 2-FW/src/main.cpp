#include <Arduino.h>
#include "PubSubClient.h"
#include <WiFi.h>
#include "Setup.h"
#include "LedsControl.cpp"
#include "AcDetectorSensor.cpp"

LedsControl ledWIFI(LEDPIN_WIFI, 100, 400);
LedsControl ledSERV(LEDPIN_SERV, 100, 400);
LedsControl ledLOW(LEDPIN_LOW, 300, 350);
AcDetectorSensor FM(SENSEPIN_FM);
AcDetectorSensor VA(SENSEPIN_VA);
AcDetectorSensor CM(SENSEPIN_CM);
WiFiClient espClient;
PubSubClient MQTT(espClient);

int count = 0;
int tentativasServer = 0; 
unsigned long previousMillisSendData;
unsigned long timeresultOK = 0;
bool state01 = false;

int nivelBateria = 0;

int testResult = 0;
int reading = 0;
int test_NOK = 1;
int test_OK1 = 2;
int test_APROVADO = 3;


bool FM_state = false;
bool VA_state = false;
bool CM_state = false;


void connectWifi() {

  if (WiFi.status() == WL_CONNECTED) {
    return;
  }

  ledWIFI.setOFF();

  Serial.print("Connecting to ");
  Serial.println(ssid);

  WiFi.enableSTA(true);
  WiFi.begin(ssid, password);

  int cont = 0;
  while (WiFi.status() != WL_CONNECTED && cont < 50) {
    cont++;
    delay(500);
    Serial.print(".");
  }

  if (cont == 50) {
      ledWIFI.setON();
      ledSERV.setON();
      ledLOW.setON();
      delay(1000);
      ESP.restart();
  }

  Serial.println();
  Serial.println("WiFi connected");
  Serial.println("IP address: ");
  Serial.println(WiFi.localIP());
}

void connectMqtt() {
  while (!MQTT.connected()) {
    ledSERV.setOFF();
    ledWIFI.setON();

    Serial.print("Connecting to MQTT Broker ");
    Serial.println(mqttServer);

    MQTT.setServer(mqttServer, 1883);
    MQTT.connect(clientId.c_str()); 


    if (MQTT.connected()){         
      //digitalWrite(status_broker,HIGH);  
      Serial.println("MQTT Conectado");
      tentativasServer=0;
      //return true;
    }

    else{
      ledSERV.setOFF();
      
      tentativasServer++;          
      Serial.print("MQTT Não Conectado. tentativa: ");
      Serial.println(tentativasServer);
    }

    if (tentativasServer >= 500){
      ESP.restart();
    }

  }
}

void keepConnection() {

  if (!MQTT.connected()) {
    connectMqtt();
  }

  connectWifi();
}

void sendData(){
  unsigned long currentMillis = millis();
  unsigned long ONTime = currentMillis/1000;

  //Serial.println("sendData");
  byte mac[6];
  WiFi.macAddress(mac);

  char macHex[17];
  sprintf(macHex, "%02X:%02X:%02X:%02X:%02X:%02X", mac[0], mac[1], mac[2], mac[3], mac[4], mac[5]);
  char params[100];
  
  count++;
  
  sprintf(params, "{\"mac\":\"%s\",\"segundos\":\"%u\",\"bateria\":\"%u\",\"FM\":\"%d\",\"VA\":\"%d\",\"CM\":\"%d\"}", macHex, ONTime, nivelBateria, FM_state, VA_state, CM_state);
  //Serial.println(params);
  
  MQTT.publish("status/teste", params);
  //MQTT.publish("status/fase", "salamaleico");

  //Serial.println("enviado");    
  //Serial.println("####################");

  

}

void pulseData(){
  unsigned long currentMillis = millis();
  
  if((currentMillis - previousMillisSendData >= 5000)){
    previousMillisSendData = currentMillis;
    unsigned long ONTime = currentMillis/1000;

    sendData();

  }

}

void fvtTester(){
  unsigned long currentMillis = millis();

  FM.isDetec();
  VA.isDetec();
  CM.isDetec();

  if (FM.isValidPulse() == true && VA.isValidPulse()==false && CM.isValidPulse()==false){
    state01 = true;   

    if (testResult == reading){
      timeresultOK = currentMillis;      
      Serial.println(currentMillis);
    }

    testResult = test_OK1;
  }
  
  else if((FM.isValidPulse()==false && testResult == reading) && (VA.isValidPulse() or CM.isValidPulse()) ){
    state01 = false; 
    
    testResult = test_NOK;
    Serial.println("<<<WHATS>>>");
  }

  if((FM.isValidPulse()==false && testResult == reading) && (VA.isValidPulse() == false or CM.isValidPulse() == false) ){
    state01 = false; 
    
    testResult = reading;
  }

  
  if (state01 == true){
    if (FM.isValidPulse()==true && (VA.isValidPulse()==false && CM.isValidPulse() == true)){
      testResult = test_APROVADO;
      //Serial.println("<<<APROVADO>>>");
    }
    else{
      if (currentMillis - timeresultOK > 5000){
        testResult = test_NOK;        
        state01 = false;
      }
    }

    
    

  }

  if (testResult != reading){    
    //timeresultOK = millis();
    int x = currentMillis - timeresultOK;

    //depuração
    Serial.print(digitalRead(SENSEPIN_FM));
    Serial.print(digitalRead(SENSEPIN_VA));
    Serial.print(digitalRead(SENSEPIN_CM));
    Serial.print(", ");
    Serial.print(FM.isValidPulse());
    Serial.print(VA.isValidPulse());
    Serial.println(CM.isValidPulse());
     
    Serial.print("primeira fase: ");
    Serial.print(state01);
    Serial.print(", testResult: ");
    Serial.print(testResult);
    Serial.print(", time: ");
    Serial.println(x);

    if (testResult == test_APROVADO){
      MQTT.publish("status/fase", "OK");
      testResult = reading;
      Serial.print("test_APROVADO");
      Serial.println(testResult);
      sys_delay_ms(4000);
    }   
    
    else if (testResult == test_NOK){
      MQTT.publish("status/fase", "NOK");
      testResult = reading;
      Serial.print("test_REAPROVADO");
      Serial.println(testResult);
      sys_delay_ms(2000);
    }

    else if(testResult == test_OK1){
      //MQTT.publish("status/fase", "ok1");
    }

    if (x > 5000){
        Serial.println("reset");
        testResult = reading;        
        state01 = false;
    }
    
  }

  


}

void inputState(){

  FM.isDetec();
  VA.isDetec();
  CM.isDetec();
  

  if (FM.isValidPulse() == true){
    FM_state = true;
    sendData();
  }
  else{
    FM_state = false;
  }
  
  if (VA.isValidPulse() == true){
    VA_state = true;
    sendData();
  }
  else{
    VA_state = false;
  }
  
  if (CM.isValidPulse() == true){
    CM_state = true;
    sendData();
  }
  else{
    CM_state = false;
  }


}

int batteryLevel(){
  int level = analogRead(SENSEPIN_BATT);
  //nivelBateria = map(level,0,4095,0,100);
  nivelBateria = map(level,0,4095,0,3300);

  if (nivelBateria < 1700){
    ledLOW.setON();
  }
  else{
    ledLOW.setOFF();
  }

  return nivelBateria;

}

void setup(){

    Serial.begin(115200);
    Serial.println("INICIANDO...");
    connectWifi();
    MQTT.setServer(mqttServer, mqttPort);
    previousMillisSendData = 0; 
}
  
void loop(){    
    keepConnection();
    
    ledWIFI.update();
    ledSERV.update();
    //ledLOW.update();
    
    batteryLevel();
    inputState();
    fvtTester();
    sys_delay_ms(500);
    //Serial.println("------------------------");
    pulseData();
    MQTT.loop();
}