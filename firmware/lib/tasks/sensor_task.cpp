#include "sensor_task.h"
#include "../config/config.h"

namespace tasks {

/**
 * @brief Estructura para pasar parámetros a la tarea
 */
struct SensorTaskParams {
    sensors::PIRSensor* sensor;
};

/**
 * @brief Función principal de la tarea del sensor PIR
 */
static void sensorTaskFunction(void *pvParameters) {
    SensorTaskParams* params = static_cast<SensorTaskParams*>(pvParameters);
    sensors::PIRSensor* sensor = params->sensor;
    delete params;
    
    Serial.println("[Sensor] Tarea iniciada");
    
    while (true) {
        // Leer estado del sensor
        sensor->isMotionDetected();
        
        // Mostrar estado cada 2 segundos para debugging
        static unsigned long lastPrint = 0;
        if (millis() - lastPrint > 2000) {
            sensor->printStatus();
            lastPrint = millis();
        }
        
        // Pequeño delay para no sobrecargar el CPU
        vTaskDelay(100 / portTICK_PERIOD_MS);
    }
}

void createSensorTask(sensors::PIRSensor& sensor, UBaseType_t priority, TaskHandle_t& taskHandle) {
    SensorTaskParams* params = new SensorTaskParams{&sensor};
    
    xTaskCreate(
        sensorTaskFunction,
        "SensorTask",
        SENSOR_TASK_STACK_SIZE,
        static_cast<void*>(params),
        priority,
        &taskHandle
    );
}

}  // namespace tasks
