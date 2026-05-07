#include <Arduino.h>
#include <WiFi.h>
#include <PubSubClient.h>
#include <freertos/FreeRTOS.h>
#include <freertos/task.h>

// Includes de configuración y módulos
#include "config/config.h"
#include <hc_sr501.h>
#include <wifi_task.h>
#include <mqtt_task.h>
#include <sensor_task.h>
#include <event_manager.h>
#include <relay.h>
#include <Led.h>
#ifdef LOGGER_API_ENABLED
#include "logger_api.h"
Logger logger = new ApiLogger();
#endif

// ========== Variables globales ==========
WiFiClient espClient;

// Handles de tareas RTOS
TaskHandle_t wifiTaskHandle = NULL;
TaskHandle_t mqttTaskHandle = NULL;
TaskHandle_t sensorTaskHandle = NULL;

// Instancia del sensor PIR
sensors::PIRSensor pirSensor(PIR_SENSOR_PIN);

// Instancia del relé
relay::Relay relayDevice(RELAY_PIN);

void setup() {
    Serial.begin(115200);
    delay(2000);  // Esperar a que el monitor serie se inicie
    
    Serial.println("\n\n========== Electronica Info ==========");
    Serial.println("Iniciando sistema...");
    Serial.println("======================================\n");
    Led::LedBuiltIn::setColor(Led::Colors::BLUE, 2000);  // Indicar inicio con LED azul
    
    // Inicializar el sensor
    pirSensor.init();
    
    // Inicializar el relé
    // relayDevice.init();
    
    // Registrar listener para eventos del relé
    events::EventManager::getInstance().subscribe(
        events::EventType::RELAY_TOGGLE,
        [](const events::Event& event) {
            Serial.print("[Main] Evento RELAY_TOGGLE recibido - Acción: ");
            Serial.println(event.actionName);
            Led::LedBuiltIn::setColor(Led::Colors::GREEN, 500);
            //relayDevice.toggle();
            //relayDevice.printStatus();
        }
    );
    
    events::EventManager::getInstance().subscribe(
        events::EventType::WIFI_CONNECTED,
        [](const events::Event& event) {
            Serial.println("[Main] Evento WIFI_CONNECTED recibido");
            Led::LedBuiltIn::setColor(Led::Colors::GREEN, 2000);
        }
    );
    
    // Crear tareas RTOS
    tasks::createWiFiTask(WIFI_TASK_PRIORITY, wifiTaskHandle);
    tasks::createMQTTTask(espClient, MQTT_TASK_PRIORITY, mqttTaskHandle);
    //tasks::createSensorTask(pirSensor, SENSOR_TASK_PRIORITY, sensorTaskHandle);
    
    Serial.println("[Main] Tareas creadas exitosamente");
    Serial.println("[Main] Sistema listo. Esperando eventos...\n");
}

void loop() {
    delay(1000);
}