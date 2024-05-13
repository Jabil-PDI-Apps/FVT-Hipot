#include <Arduino.h>

//PINOS
#define LEDPIN_WIFI      32
#define LEDPIN_SERV      25
#define LEDPIN_LOW       33
#define SENSEPIN_FM      26//27
#define SENSEPIN_VA      14//14
#define SENSEPIN_CM      27//26
#define SENSEPIN_BATT    35

//WIFI
//const char* ssid = "ITWeb";
//const char* password = "indt2018";
//const char* ssid = "jabil_testers";
//const char* password = "webT3st@M4N!";
const char* ssid = "jabilrf";
const char* password = "Manrf#S4p";

//MQTT
//const char* mqttServer = "BrokerFVT";
//const char* mqttServer = "10.60.70.195";
const char* mqttServer = "10.56.253.155";
const int mqttPort = 1883;
const char* mqttUser = "FVT_TESTER_IOT";
const char* mqttPassword = "webT3st@M4N!";
//String clientId = "FVT_TESTER_K9-v1";
String clientId = "FVT_TESTER_K9-v1";
