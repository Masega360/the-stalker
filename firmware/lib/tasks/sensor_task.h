#ifndef SENSOR_TASK_H
#define SENSOR_TASK_H

#include <freertos/FreeRTOS.h>
#include <freertos/task.h>
#include "../sensors/hc_sr501.h"

namespace tasks {

/**
 * @brief Crea la tarea de lectura del sensor PIR
 * @param sensor Instancia del sensor PIR
 * @param priority Prioridad de la tarea RTOS
 * @param taskHandle Referencia al handle de la tarea
 */
void createSensorTask(sensors::PIRSensor& sensor, UBaseType_t priority, TaskHandle_t& taskHandle);

}  // namespace tasks

#endif // SENSOR_TASK_H
