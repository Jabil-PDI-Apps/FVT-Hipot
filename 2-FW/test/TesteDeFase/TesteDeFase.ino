
#include <WiFi.h>
#include <PubSubClient.h>
#define status_wifi 23
#define status_broker 22
#define status_teste_ok 17
#define status_teste_ng 5
#define input_teste 4

WiFiClient espClient;
PubSubClient client(espClient);

const char* mqtt_server = "10.56.255.30";
const char* ssid = "jabil_testers";
const char* password = "webT3st@M4N!";

unsigned long tempo;
bool st=false,wifi=false,mqtt=false;


void testeReset();
bool setup_mqtt();
bool setup_wifi();


void setup()
{
    Serial.begin(115200);
    pinMode(input_teste,INPUT_PULLUP);
    pinMode(status_wifi,OUTPUT);
    pinMode(status_teste_ok,OUTPUT);
    pinMode(status_teste_ng,OUTPUT);
    pinMode(status_broker,OUTPUT);
    digitalWrite(status_wifi,LOW);
    
    delay(1);
    wifi=setup_wifi();
    mqtt=setup_mqtt();
    
}

char c;
int contador=0;
String txt="";
char buff[10];


void loop()
{   
    

    if(WiFi.status() == WL_CONNECTED){
     
      wifi=true;
      if (digitalRead(input_teste)==0){
        testeReset();
        Serial.println("Entrou");
        txt=(String)contador;
        txt.toCharArray(buff,10);
        
        if (client.connected()){
          mqtt=true;
          client.publish("status/fase",buff);
          digitalWrite(status_broker,HIGH); 
          tempo=millis();  
          
          while(millis()-tempo<=4000){
            
            if(st){
              digitalWrite(status_teste_ok,LOW);
              digitalWrite(status_teste_ng,HIGH);
            }
            
            else{
              digitalWrite(status_teste_ok,HIGH);
              digitalWrite(status_teste_ng,LOW);
            }

            delay(100);
            st=!st;
            
          }
          
          if(contador%2==0){
            digitalWrite(status_teste_ok,LOW);
            digitalWrite(status_teste_ng,HIGH);
          }
          else{
            digitalWrite(status_teste_ok,HIGH);
            digitalWrite(status_teste_ng,LOW);
          }
          
        }
        
        else{
          
          digitalWrite(status_broker,LOW);
          
          mqtt=setup_mqtt();
         
         }
        
        contador+=1;
       }
    
    }
    else{
      digitalWrite(status_wifi,LOW);
      wifi=setup_wifi();
    }
    if(client.connected()==false){
      mqtt=setup_mqtt();  
    }
    else{
      client.publish("status/fase","salamaleico");
      delay(2000);
     }
    
}

bool setup_wifi() {
  delay(10);
  
  Serial.println();
  Serial.print("Connecting to ");
  Serial.println(ssid);

  WiFi.begin(ssid, password);

  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }

  Serial.println("");
  Serial.println("WiFi connected");
  Serial.println("IP address: ");
  Serial.println(WiFi.localIP());
  digitalWrite(status_wifi,HIGH);
  return true;
}

bool setup_mqtt(){
  Serial.println("Conectando MQTT");
  client.setServer(mqtt_server, 1883);
  client.connect("ESP32Client");  
  if (client.connected()){         
    digitalWrite(status_broker,HIGH);  
    Serial.println("MQTT Conectado");
    return true;
  }

  else{
    digitalWrite(status_broker,LOW);
    Serial.println("MQTT Não Conectado");
    return false;  
      
  }
}

void testeReset(){
    digitalWrite(status_teste_ok,LOW);
    digitalWrite(status_teste_ng,LOW);
}
