#ifndef CONFIG_H
#define CONFIG_H

// ========== WiFi Configuration ==========
static constexpr const char* WIFI_SSID = "DHIPOPC";
static constexpr const char* WIFI_PASSWORD = "123456789";

// ========== MQTT Configuration ==========
static constexpr const char* MQTT_SERVER = "3.218.237.212";
static constexpr int MQTT_PORT = 1883;
static constexpr const char* MQTT_CLIENT_ID = "ESP32-CAM-01";
static constexpr const char* MQTT_STATUS_TOPIC = "/status";

// ========== Sensor Configuration ==========
static constexpr int PIR_SENSOR_PIN = 5;  // GPIO5 para el sensor HC-SR501

// ========== Relay Configuration ==========
static constexpr int RELAY_PIN = 27;  // GPIO27 para el relé

// ========== Task Configuration ==========
static constexpr int WIFI_TASK_STACK_SIZE = 4096;
static constexpr int MQTT_TASK_STACK_SIZE = 4096;
static constexpr int SENSOR_TASK_STACK_SIZE = 2048;
static constexpr int CAMERA_TASK_STACK_SIZE = 8192;

static constexpr int WIFI_TASK_PRIORITY = 1;
static constexpr int MQTT_TASK_PRIORITY = 1;
static constexpr int SENSOR_TASK_PRIORITY = 2;
static constexpr int CAMERA_TASK_PRIORITY = 2;

static constexpr int CAMERA_FRAME_INTERVAL_MS = 500; // 2 FPS por defecto

#endif // CONFIG_H
