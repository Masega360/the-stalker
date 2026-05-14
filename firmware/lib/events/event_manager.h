#ifndef EVENT_MANAGER_H
#define EVENT_MANAGER_H

#include "event.h"
#include <map>
#include <vector>

namespace events {

/**
 * @class EventManager
 * @brief Gestor central de eventos de la aplicación
 * 
 * Permite registrar listeners para tipos de eventos específicos
 * y disparar eventos que serán procesados por todos los listeners registrados.
 */
class EventManager {
private:
    // Mapa de tipo de evento a lista de callbacks
    std::map<EventType, std::vector<EventCallback>> listeners;
    
    // Instancia singleton
    static EventManager* instance;
    
    // Constructor privado para patrón singleton
    EventManager() = default;

public:
    // Prevenir copia
    EventManager(const EventManager&) = delete;
    EventManager& operator=(const EventManager&) = delete;

    /**
     * @brief Obtiene la instancia singleton del EventManager
     * @return Referencia al EventManager
     */
    static EventManager& getInstance();

    /**
     * @brief Registra un listener para un tipo de evento
     * @param eventType Tipo de evento a escuchar
     * @param callback Función a ejecutar cuando ocurra el evento
     */
    void subscribe(EventType eventType, EventCallback callback);

    /**
     * @brief Dispara un evento
     * @param event El evento a disparar
     */
    void emit(const Event& event);

    /**
     * @brief Dispara un evento por tipo y nombre de acción
     * @param eventType Tipo de evento
     * @param actionName Nombre de la acción
     * @param payload Datos adicionales (opcional)
     */
    void emit(EventType eventType, const char* actionName, const char* payload = nullptr);

    /**
     * @brief Dispara un evento con datos binarios
     * @param eventType Tipo de evento
     * @param data Puntero a datos binarios
     * @param dataLen Longitud de los datos
     */
    void emit(EventType eventType, void* data, size_t dataLen);

    /**
     * @brief Limpia todos los listeners registrados
     */
    void clear();

    /**
     * @brief Imprime información de debug sobre los listeners registrados
     */
    void printStatus();
};

}  // namespace events

#endif // EVENT_MANAGER_H
