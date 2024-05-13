#include <Arduino.h>

class AcDetectorSensor{

  #define CURRENT 0
  #define PREVIOUS 1
  #define CHANGED 2
  #define DETECTED  false
  #define NO_DETECT true
  #define TEMPO_DEBOUNCE 100
  #define TEMPO_BT_PRESSED_MAX 3000


  private: 
  uint8_t sensorPin;
  uint8_t mode;
  uint8_t state;  
  uint8_t stateDebug; 
  uint8_t stateValided; 
   
  unsigned long int changegTime;
 
  public:
  AcDetectorSensor(int pin){
    sensorPin = pin;
    pinMode(sensorPin, INPUT);     
    state = 0; 
    changegTime = 0;
  }

  bool isDetec(){
    bitWrite(state,PREVIOUS,bitRead(state,CURRENT));
    if (digitalRead(sensorPin) == NO_DETECT){
        bitWrite(state,CURRENT,NO_DETECT);
    } else {
        bitWrite(state,CURRENT,DETECTED);
    }
    if (bitRead(state,CURRENT) != bitRead(state,PREVIOUS)){
        bitWrite(state,CHANGED,DETECTED);
    }else{
        bitWrite(state,CHANGED,NO_DETECT);
    }
    stateDebug = bitRead(state,CURRENT);
	return bitRead(state,CURRENT);
}

  bool wasPressed(void){
      if (bitRead(state,CURRENT)){
          return true;
      } else {
          return false;
      }
  }

  bool stateChanged(void){
      return bitRead(state,CHANGED);
  }


  bool uniquePress(void){
      return (isDetec() && stateChanged());
  }

  bool isValidPulse(){
    unsigned long currentMillis = millis();

    if (stateChanged()){
      changegTime = currentMillis;
    }

    if ( currentMillis - changegTime > TEMPO_DEBOUNCE) {
      if (isDetec() == DETECTED){
        //Serial.print(sensorPin);
        //Serial.print(": ");
        //Serial.print(stateDebug);
        //Serial.print(", ");
        //Serial.println(stateValided);
        stateValided = true;
      }
    
      else{          
          //Serial.print(sensorPin);
          //Serial.print(": ");
          //Serial.print(stateDebug);
          //Serial.print(", ");
          //Serial.println(stateValided);
          stateValided = false;
      }
    }
    return stateValided;
  }
};