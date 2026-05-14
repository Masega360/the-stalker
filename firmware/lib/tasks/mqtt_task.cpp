#include "mqtt_task.h"
#include "wifi_task.h"
#include "../config/config.h"
#include "../events/event_manager.h"
#ifdef DEVICE_ROLE_CAMERA
#include "esp_camera.h"
#endif

namespace tasks {

// Variable global para almacenar la instancia del cliente MQTT
static PubSubClient mqttClient;

/**
 * @brief Callback MQTT que se ejecuta cuando se recibe un mensaje
 */
static void onMqttMessage(char* topic, byte* payload, unsigned int length) {
    // Convertir payload a string
    char payloadStr[256];
    if (length < sizeof(payloadStr)) {
        memcpy(payloadStr, payload, length);
        payloadStr[length] = '\0';
    } else {
        payloadStr[0] = '\0';
    }
    
    Serial.print("[MQTT] Mensaje recibido - Topic: ");
    Serial.print(topic);
    Serial.print(" | Payload: ");
    Serial.println(payloadStr);
    
    // Parsear topic para obtener el nombre de la acción
    // Formato esperado: {clientId}/actions/{actionName}
    String topicStr(topic);
    int actionsIndex = topicStr.indexOf("/actions/");
    if (actionsIndex != -1) {
        String actionName = topicStr.substring(actionsIndex + 9);
        
        // Disparar evento según la acción
        if (actionName == "relay") {
            events::EventManager::getInstance().emit(
                events::EventType::RELAY_TOGGLE,
                actionName.c_str(),
                payloadStr
            );
        } else if (actionName == "take_photo") {
            events::EventManager::getInstance().emit(
                events::EventType::TAKE_PHOTO,
                actionName.c_str(),
                payloadStr
            );
        }
    }
}

/**
 * @brief Función principal de la tarea MQTT
 */
static void mqttTaskFunction(void *pvParameters) {
    // Esperar a que WiFi esté conectado
    while (!isWiFiConnected()) {
        Serial.println("[MQTT] Esperando conexión WiFi...");
        vTaskDelay(1000 / portTICK_PERIOD_MS);
    }
    
    mqttClient.setServer(MQTT_SERVER, MQTT_PORT);
    mqttClient.setBufferSize(MQTT_MAX_PACKET_SIZE); // Asegurar buffer para fotos
    mqttClient.setCallback(onMqttMessage);
    Serial.println("[MQTT] Servidor configurado");

    // Suscribirse a eventos de fotos capturadas
    events::EventManager::getInstance().subscribe(
        events::EventType::PHOTO_CAPTURED,
        [](const events::Event& event) {
            if (mqttClient.connected() && event.data != nullptr) {
                String photoTopic = String("/") + MQTT_CLIENT_ID + "/camera/photo";
                
#ifdef DEVICE_ROLE_CAMERA
                camera_fb_t* fb = (camera_fb_t*)event.data;
                Serial.printf("[MQTT] Publicando foto en %s (%d bytes)\n", photoTopic.c_str(), fb->len);
                
                bool success = mqttClient.publish(photoTopic.c_str(), fb->buf, fb->len);
                if (!success) {
                    Serial.println("[MQTT] ✗ Fallo al publicar foto (¿Payload demasiado grande?)");
                }
                
                // LIBERAR el buffer de la cámara
                esp_camera_fb_return(fb);
#endif
            }
        }
    );
    
    while (true) {
        if (!mqttClient.connected()) {
            Serial.println("[MQTT] Intentando conectar...");
            if (mqttClient.connect(MQTT_CLIENT_ID)) {
                Serial.println("[MQTT] ✓ Conectado");
                // Suscribirse al topic de acciones
                mqttClient.publish("register/cam", MQTT_CLIENT_ID);
                Serial.println("[MQTT] ✓ Registrado en /register/cam");
                mqttClient.publish(
                    (String(MQTT_CLIENT_ID) + String(MQTT_STATUS_TOPIC)).c_str(),
                    "online"
                );
                Serial.println("[MQTT] ✓ Publicado estado online");
                mqttClient.subscribe(
                    (String(MQTT_CLIENT_ID) + String("/actions/#")).c_str()
                );
                Serial.println("[MQTT] ✓ Suscrito a /actions/#");
            } else {
                Serial.print("[MQTT] ✗ Error: ");
                Serial.println(mqttClient.state());
                vTaskDelay(5000 / portTICK_PERIOD_MS);
            }
        }


        mqttClient.loop();
        vTaskDelay(10 / portTICK_PERIOD_MS);
    }
}

void createMQTTTask(WiFiClient& espClient, UBaseType_t priority, TaskHandle_t& taskHandle) {
    mqttClient.setClient(espClient);
    
    xTaskCreate(
        mqttTaskFunction,
        "MQTTTask",
        MQTT_TASK_STACK_SIZE,
        NULL,
        priority,
        &taskHandle
    );
}

bool isMQTTConnected() {
    return mqttClient.connected();
}

PubSubClient& getMQTTClient() {
    return mqttClient;
}

}  // namespace tasks
