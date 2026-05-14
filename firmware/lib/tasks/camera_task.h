#ifndef CAMERA_TASK_H
#define CAMERA_TASK_H

#include <freertos/FreeRTOS.h>
#include <freertos/task.h>

namespace tasks {

/**
 * @brief Crea la tarea de captura de cámara
 * @param priority Prioridad de la tarea RTOS
 * @param taskHandle Referencia al handle de la tarea
 */
void createCameraTask(UBaseType_t priority, TaskHandle_t& taskHandle);

}  // namespace tasks

#endif // CAMERA_TASK_H
