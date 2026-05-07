#ifndef RELAY_H
#define RELAY_H

#include <Arduino.h>

namespace relay {

/**
 * @class Relay
 * @brief Controlador para un relé conectado a un pin GPIO
 * 
 * Permite controlar un relé (encender, apagar, conmutar)
 * y monitorear su estado.
 */
class Relay {
private:
    int relayPin;           // Pin GPIO del relé
    bool isOn;              // Estado actual del relé
    unsigned long lastChangeTime;  // Timestamp del último cambio

public:
    /**
     * @brief Constructor del relé
     * @param pin Pin GPIO donde está conectado el relé
     */
    Relay(int pin);

    /**
     * @brief Inicializa el relé
     */
    void init();

    /**
     * @brief Enciende el relé
     */
    void on();

    /**
     * @brief Apaga el relé
     */
    void off();

    /**
     * @brief Conmuta el relé (enciende si estaba apagado, apaga si estaba encendido)
     */
    void toggle();

    /**
     * @brief Obtiene el estado actual del relé
     * @return true si está encendido, false si está apagado
     */
    bool getState() const;

    /**
     * @brief Imprime el estado actual del relé en Serial
     */
    void printStatus();
};

}  // namespace relay

#endif // RELAY_H
