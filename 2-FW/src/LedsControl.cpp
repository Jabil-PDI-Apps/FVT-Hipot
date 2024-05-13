#include <Arduino.h>

class LedsControl{

  int ledPin;      // número do pino do LED
  long OnTime;     // milissegundos do tempo ligado
  long OffTime;    // milissegundos do tempo desligado

  // Essas mantém o estado atual
  int ledState;                     // ledState usada para guardar o estado do LED
  unsigned long previousMillis;      // vai guardar o último acionamento do LED
 
  public:
  LedsControl(int pin, long on, long off){
    ledPin = pin;
    pinMode(ledPin, OUTPUT);     
       
    OnTime = on;
    OffTime = off;
     
    ledState = LOW; 
    previousMillis = 0;
  }
 
  void update(){
    // Faz a checagem para saber se já é o momento de alterar o estado do LED
    unsigned long currentMillis = millis();

    if((ledState == HIGH) && (currentMillis - previousMillis >= OnTime)){
      ledState = LOW;  // Desliga o LED
      previousMillis = currentMillis;  // Guarda o tempo
      digitalWrite(ledPin, ledState);  // Faz o Update do LED
    }

    else if ((ledState == LOW) && (currentMillis - previousMillis >= OffTime)){
      ledState = HIGH;  // Liga o LED
      previousMillis = currentMillis;   //Guarda o tempo
      digitalWrite(ledPin, ledState);      // Faz o Update do LED
    }

  }

  void setON(){
    ledState = HIGH;
    digitalWrite(ledPin, ledState);
  }

  void setOFF(){
    ledState = LOW;
    digitalWrite(ledPin, ledState);
  }


};
 
