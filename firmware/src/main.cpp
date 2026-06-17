#include <Arduino.h>
#include <WiFi.h>
#include <PubSubClient.h>
#include <freertos/FreeRTOS.h>
#include <freertos/task.h>

// Includes de configuración y módulos
#include "config/config.h"
#include <wifi_task.h>
#include <mqtt_task.h>
#include <event_manager.h>
#include <Led.h>

#ifdef DEVICE_ROLE_ACTOR
#include <relay.h>
#endif

#ifdef DEVICE_ROLE_CAMERA
#include <hc_sr501.h>
#include <sensor_task.h>
#include <camera_task.h>
#endif

#ifdef LOGGER_API_ENABLED
#include "logger_api.h"
Logger logger = new ApiLogger();
#endif

// ========== Variables globales ==========
WiFiClient espClient;

// Handles de tareas RTOS
TaskHandle_t wifiTaskHandle = NULL;
TaskHandle_t mqttTaskHandle = NULL;

#ifdef DEVICE_ROLE_ACTOR
relay::Relay relayDevice(RELAY_PIN);
#endif

#ifdef DEVICE_ROLE_CAMERA
TaskHandle_t sensorTaskHandle = NULL;
sensors::PIRSensor pirSensor(PIR_SENSOR_PIN);
TaskHandle_t cameraTaskHandle = NULL;
#endif

void setup() {
    Serial.begin(115200);
    delay(2000);
    
    Serial.println("\n\n========== ESP32 Role-Based Firmware ==========");
#ifdef DEVICE_ROLE_ACTOR
    Serial.println("Role: ACTOR (Relay & Sensors)");
#elif defined(DEVICE_ROLE_CAMERA)
    Serial.println("Role: CAMERA (MQTT Streamer)");
#else
    Serial.println("Role: UNDEFINED (Check build flags)");
#endif
    Serial.println("==============================================\n");

    Led::LedBuiltIn::setColor(Led::Colors::BLUE, 2000);
    
#ifdef DEVICE_ROLE_ACTOR
    relayDevice.init();
    relayDevice.toggle(); // abro
    delay(2000);
    relayDevice.toggle(); // cierro para probar
    
    events::EventManager::getInstance().subscribe(
        events::EventType::RELAY_TOGGLE,
        [](const events::Event& event) {
            Serial.print("[Main] Evento RELAY_TOGGLE recibido");
            Led::LedBuiltIn::setColor(Led::Colors::GREEN, 500);
            relayDevice.toggle();
        }
    );
#endif

#ifdef DEVICE_ROLE_CAMERA
    pirSensor.init();
#endif

    events::EventManager::getInstance().subscribe(
        events::EventType::WIFI_CONNECTED,
        [](const events::Event& event) {
            Serial.println("[Main] Evento WIFI_CONNECTED recibido");
            Led::LedBuiltIn::setColor(Led::Colors::GREEN, 2000);
        }
    );
    
    // Crear tareas comunes
    tasks::createWiFiTask(WIFI_TASK_PRIORITY, wifiTaskHandle);
    tasks::createMQTTTask(espClient, MQTT_TASK_PRIORITY, mqttTaskHandle);

#ifdef DEVICE_ROLE_CAMERA
    // tasks::createSensorTask(pirSensor, SENSOR_TASK_PRIORITY, sensorTaskHandle);
    tasks::createCameraTask(CAMERA_TASK_PRIORITY, cameraTaskHandle);
#endif
    
    Serial.println("[Main] Tareas creadas exitosamente");
    Serial.println("[Main] Sistema listo. Esperando eventos...\n");
}

void loop() {
    vTaskDelay(pdMS_TO_TICKS(1000));
}
