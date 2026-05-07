#ifndef HC_SR501_H
#define HC_SR501_H

#include <Arduino.h>

namespace sensors {

/**
 * @class PIRSensor
 * @brief Controlador para el sensor de movimiento HC-SR501
 * 
 * El HC-SR501 es un sensor PIR que detecta cambios en radiación infrarroja.
 * Retorna HIGH cuando detecta movimiento, LOW cuando no detecta.
 */
class PIRSensor {
private:
    int sensorPin;          // Pin GPIO del sensor
    bool lastState;         // Último estado registrado
    unsigned long lastChangeTime;  // Tiempo del último cambio

public:
    /**
     * @brief Constructor del sensor PIR
     * @param pin Pin GPIO donde está conectado el sensor
     */
    PIRSensor(int pin);

    /**
     * @brief Inicializa el sensor
     */
    void init();

    /**
     * @brief Lee el estado actual del sensor
     * @return true si detecta movimiento, false si no
     */
    bool isMotionDetected();

    /**
     * @brief Obtiene el último estado registrado
     * @return true si había movimiento, false si no
     */
    bool getLastState() const;

    /**
     * @brief Imprime el estado actual del sensor en Serial
     */
    void printStatus();
};

}  // namespace sensors

#endif // HC_SR501_H
