#include "relay.h"

namespace relay {

Relay::Relay(int pin) : relayPin(pin), isOn(false), lastChangeTime(0) {
}

void Relay::init() {
    pinMode(relayPin, OUTPUT);
    digitalWrite(relayPin, LOW);  // Inicialmente apagado
    isOn = false;
    Serial.print("[Relay] Inicializado en pin: ");
    Serial.println(relayPin);
}

void Relay::on() {
    if (!isOn) {
        digitalWrite(relayPin, HIGH);
        isOn = true;
        lastChangeTime = millis();
        Serial.print("[Relay] Activado (ON)");
        Serial.println();
    }
}

void Relay::off() {
    if (isOn) {
        digitalWrite(relayPin, LOW);
        isOn = false;
        lastChangeTime = millis();
        Serial.print("[Relay] Desactivado (OFF)");
        Serial.println();
    }
}

void Relay::toggle() {
    if (isOn) {
        off();
    } else {
        on();
    }
}

bool Relay::getState() const {
    return isOn;
}

void Relay::printStatus() {
    Serial.print("[Relay] Estado: ");
    Serial.print(isOn ? "ON (ENCENDIDO)" : "OFF (APAGADO)");
    Serial.print(" | Último cambio: ");
    Serial.print(millis() - lastChangeTime);
    Serial.println(" ms atrás");
}

}  // namespace relay
