#ifndef WIFI_TASK_H
#define WIFI_TASK_H

#include <freertos/FreeRTOS.h>
#include <freertos/task.h>

namespace tasks {

/**
 * @brief Crea la tarea de conexión a WiFi
 * @param priority Prioridad de la tarea RTOS
 * @param taskHandle Referencia al handle de la tarea
 */
void createWiFiTask(UBaseType_t priority, TaskHandle_t& taskHandle);

/**
 * @brief Verifica si está conectado a WiFi
 * @return true si está conectado, false si no
 */
bool isWiFiConnected();

}  // namespace tasks

#endif // WIFI_TASK_H
