#include "hc_sr501.h"

namespace sensors {

PIRSensor::PIRSensor(int pin) : sensorPin(pin), lastState(false), lastChangeTime(0) {
}

void PIRSensor::init() {
    pinMode(sensorPin, INPUT);
    Serial.print("Sensor HC-SR501 inicializado en pin: ");
    Serial.println(sensorPin);
}

bool PIRSensor::isMotionDetected() {
    bool currentState = digitalRead(sensorPin) == HIGH;
    
    // Actualizar estado si cambió
    if (currentState != lastState) {
        lastState = currentState;
        lastChangeTime = millis();
    }
    
    return currentState;
}

bool PIRSensor::getLastState() const {
    return lastState;
}

void PIRSensor::printStatus() {
    Serial.print("Estado PIR: ");
    Serial.print(lastState ? "MOVIMIENTO DETECTADO" : "SIN MOVIMIENTO");
    Serial.print(" | Último cambio hace: ");
    Serial.print(millis() - lastChangeTime);
    Serial.println(" ms");
}

}  // namespace sensors
