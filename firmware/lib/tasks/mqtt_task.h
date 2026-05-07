#ifndef MQTT_TASK_H
#define MQTT_TASK_H

#include <freertos/FreeRTOS.h>
#include <freertos/task.h>
#include <PubSubClient.h>
#include <WiFiClient.h>

namespace tasks {

/**
 * @brief Crea la tarea de conexión a MQTT
 * @param espClient Cliente WiFi para MQTT
 * @param priority Prioridad de la tarea RTOS
 * @param taskHandle Referencia al handle de la tarea
 */
void createMQTTTask(WiFiClient& espClient, UBaseType_t priority, TaskHandle_t& taskHandle);

/**
 * @brief Verifica si está conectado a MQTT
 * @return true si está conectado, false si no
 */
bool isMQTTConnected();

/**
 * @brief Obtiene la instancia del cliente MQTT
 * @return Referencia al cliente MQTT
 */
PubSubClient& getMQTTClient();

}  // namespace tasks

#endif // MQTT_TASK_H
