#ifndef EVENT_H
#define EVENT_H

#include <Arduino.h>
#include <functional>

namespace events {

/**
 * @enum EventType
 * @brief Enumeración de tipos de eventos disponibles
 */
enum class EventType {
    RELAY_TOGGLE,      // Conmutar relé
    RELAY_ON,          // Encender relé
    RELAY_OFF,         // Apagar relé
    MOTION_DETECTED,   // Movimiento detectado
    MOTION_STOPPED,    // Movimiento parado
    WIFI_CONNECTED,    // WiFi conectado
    WIFI_DISCONNECTED, // WiFi desconectado
    CUSTOM             // Evento personalizado
};

/**
 * @struct Event
 * @brief Estructura que representa un evento
 */
struct Event {
    EventType type;              // Tipo de evento
    const char* actionName;      // Nombre de la acción (ej: "toggle", "on", "off")
    const char* payload;         // Datos adicionales del evento
    unsigned long timestamp;     // Timestamp del evento
    
    Event(EventType type, const char* actionName = nullptr, const char* payload = nullptr)
        : type(type), actionName(actionName), payload(payload), timestamp(millis()) {}
};

// Tipo de callback para manejar eventos
using EventCallback = std::function<void(const Event&)>;

}  // namespace events

#endif // EVENT_H
