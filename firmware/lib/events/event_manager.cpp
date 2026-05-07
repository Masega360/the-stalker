#include "event_manager.h"

namespace events {

EventManager* EventManager::instance = nullptr;

EventManager& EventManager::getInstance() {
    if (instance == nullptr) {
        instance = new EventManager();
    }
    return *instance;
}

void EventManager::subscribe(EventType eventType, EventCallback callback) {
    listeners[eventType].push_back(callback);
    Serial.print("[EventManager] Listener registrado para tipo: ");
    Serial.println(static_cast<int>(eventType));
}

void EventManager::emit(const Event& event) {
    Serial.print("[EventManager] Evento disparado: ");
    Serial.print("Tipo=");
    Serial.print(static_cast<int>(event.type));
    Serial.print(" Acción=");
    Serial.println(event.actionName ? event.actionName : "N/A");

    auto it = listeners.find(event.type);
    if (it != listeners.end()) {
        for (auto& callback : it->second) {
            callback(event);
        }
    }
}

void EventManager::emit(EventType eventType, const char* actionName, const char* payload) {
    Event event(eventType, actionName, payload);
    emit(event);
}

void EventManager::clear() {
    listeners.clear();
    Serial.println("[EventManager] Todos los listeners han sido limpiados");
}

void EventManager::printStatus() {
    Serial.println("\n========== EventManager Status ==========");
    Serial.print("Total tipos de eventos registrados: ");
    Serial.println(listeners.size());
    
    for (auto& pair : listeners) {
        Serial.print("EventType ");
        Serial.print(static_cast<int>(pair.first));
        Serial.print(": ");
        Serial.print(pair.second.size());
        Serial.println(" listeners");
    }
    Serial.println("========================================\n");
}

}  // namespace events
