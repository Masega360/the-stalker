#ifndef CONFIG_H
#define CONFIG_H

// ========== WiFi Configuration ==========
static constexpr const char* WIFI_SSID = "DHIPOPC";
static constexpr const char* WIFI_PASSWORD = "123456789";

// ========== MQTT Configuration ==========
static constexpr const char* MQTT_SERVER = "3.218.237.212";
static constexpr int MQTT_PORT = 1883;
static constexpr const char* MQTT_STATUS_TOPIC = "/status";

// ========== Device Registration ==========
#ifdef DEVICE_ROLE_CAMERA
static constexpr const char* DEVICE_ID = "CAM-0000";
static constexpr const char* MQTT_CLIENT_ID = "CAM-0000";
static constexpr const char* MQTT_REGISTER_TOPIC = "/register/cam";
#elif defined(DEVICE_ROLE_ACTOR)
static constexpr const char* DEVICE_ID = "ACT-0000";
static constexpr const char* MQTT_CLIENT_ID = "ACT-0000";
static constexpr const char* MQTT_REGISTER_TOPIC = "/register/actor";
#endif

// ========== Sensor Configuration ==========
static constexpr int PIR_SENSOR_PIN = 14;  // GPIO14 para el sensor HC-SR501

// ========== Relay Configuration ==========
static constexpr int RELAY_PIN = 33;  // GPIO33 para el relé

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
