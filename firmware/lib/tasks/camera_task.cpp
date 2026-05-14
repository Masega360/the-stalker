#include "camera_task.h"
#include "../camera/esp32_cam.h"
#include "../events/event_manager.h"
#include "../config/config.h"

namespace tasks {

static bool streamingEnabled = true;

static void cameraTaskFunction(void *pvParameters) {
    Serial.println("[CameraTask] Iniciando...");
    
    if (!camera::initCamera()) {
        Serial.println("[CameraTask] ✗ Fallo al inicializar cámara. Terminando tarea.");
        vTaskDelete(NULL);
        return;
    }

    while (true) {
        if (streamingEnabled) {
            Serial.println("[CameraTask] Capturando frame...");
            camera_fb_t* fb = camera::captureFrame();
            if (fb) {
                Serial.printf("[CameraTask] Frame capturado: %d bytes\n", fb->len);
                // Emitir evento con el puntero a la estructura camera_fb_t
                events::EventManager::getInstance().emit(
                    events::EventType::PHOTO_CAPTURED,
                    (void*)fb,
                    fb->len
                );
            } else {
                Serial.println("[CameraTask] ✗ Fallo al capturar frame");
            }
        }
        
        vTaskDelay(pdMS_TO_TICKS(CAMERA_FRAME_INTERVAL_MS));
    }
}

void createCameraTask(UBaseType_t priority, TaskHandle_t& taskHandle) {
    xTaskCreate(
        cameraTaskFunction,
        "CameraTask",
        CAMERA_TASK_STACK_SIZE,
        NULL,
        priority,
        &taskHandle
    );
}

}  // namespace tasks
