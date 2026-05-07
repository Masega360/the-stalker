#include "wifi_task.h"
#include <WiFi.h>
#include "../config/config.h"
#include "../events/event_manager.h"

namespace tasks {

/**
 * @brief Función principal de la tarea WiFi
 */
static void wifiTaskFunction(void *pvParameters) {
    Serial.println("[WiFi] Conectando a WiFi...");
    WiFi.begin(WIFI_SSID, WIFI_PASSWORD);
    
    int attempts = 0;
    while (WiFi.status() != WL_CONNECTED && attempts < 50) {
        Serial.print(".");
        vTaskDelay(1000 / portTICK_PERIOD_MS);
        attempts++;
    }
    
    if (WiFi.status() == WL_CONNECTED) {
        Serial.println("\n[WiFi] ✓ Conectado");
        Serial.print("[WiFi] IP: ");
        Serial.println(WiFi.localIP());
        events::EventManager::getInstance().emit(
            events::EventType::WIFI_CONNECTED, 
            "connected",
            WiFi.localIP().toString().c_str()
        );
    } else {
        Serial.println("\n[WiFi] ✗ No se pudo conectar");
    }
    
    // Tarea completada, se elimina a sí misma
    vTaskDelete(NULL);
}

void createWiFiTask(UBaseType_t priority, TaskHandle_t& taskHandle) {
    xTaskCreate(
        wifiTaskFunction,
        "WiFiTask",
        WIFI_TASK_STACK_SIZE,
        NULL,
        priority,
        &taskHandle
    );
}

bool isWiFiConnected() {
    return WiFi.status() == WL_CONNECTED;
}

}  // namespace tasks
