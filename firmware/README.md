# 🔌 Electronica Info - Sistema IoT Modular para ESP32

Un sistema IoT modular y escalable basado en ESP32 que utiliza **FreeRTOS**, **MQTT** y arquitectura **event-driven** para optimizar el uso de recursos del microcontrolador.

## ✨ Características Principales

✅ **Arquitectura Modular** - Código separado en componentes independientes y reutilizables  
✅ **Event-Driven** - Sistema de eventos centralizado para desacoplar componentes  
✅ **RTOS Tasks** - Uso de tareas FreeRTOS para paralelismo y optimización de recursos  
✅ **MQTT Integration** - Conectividad completa con broker MQTT vía WiFi  
✅ **Configuración Centralizada** - Todos los parámetros en un único archivo  
✅ **Fácil Extensión** - Agregar sensores, actuadores y acciones es simple  

## 🏗️ Arquitectura

El sistema está dividido en módulos independientes:

```
┌─────────────────────────────────┐
│    MQTT Broker (test.mosquitto) │
└────────────┬────────────────────┘
             │
             ↓
┌─────────────────────────────────┐
│      MQTT Task (RTOS)           │
│  - Conecta a WiFi               │
│  - Conecta a broker MQTT        │
│  - Suscribe a /actions/#        │
│  - Parsea y dispara eventos     │
└────────────┬────────────────────┘
             │
             ↓
┌─────────────────────────────────┐
│    Event Manager (Singleton)    │
│  - Gestiona listeners           │
│  - Dispara eventos              │
│  - Desacopla componentes        │
└────────────┬────────────────────┘
             │
      ┌──────┴──────┐
      ↓             ↓
  ┌────────┐   ┌─────────┐
  │ Relé   │   │ Sensores│
  │Handler │   │ Tasks   │
  └────────┘   └─────────┘
```

## 🔌 Hardware

### Componentes Utilizados

| Componente | Pin GPIO | Descripción |
|-----------|----------|-------------|
| **HC-SR501 PIR** | GPIO5 | Sensor de movimiento infrarrojo |
| **Relé** | GPIO27 | Control de carga (luz, motor, etc.) |
| **ESP32** | - | Microcontrolador dual-core |

### Esquema de Conexión

```
HC-SR501 PIR Sensor        Relay Module
┌─────────────┐           ┌──────────────┐
│ VCC → 5V    │           │ VCC → 5V     │
│ GND → GND   │           │ GND → GND    │
│ OUT → GPIO5 │           │ IN → GPIO27  │
└─────────────┘           └──────────────┘
```

## 📋 Estructura del Proyecto

```
Electronica Info/
├── include/
│   └── config/
│       └── config.h              # Configuraciones centralizadas
├── lib/
│   ├── sensors/
│   │   ├── hc_sr501.h           # Interfaz sensor PIR
│   │   └── hc_sr501.cpp         # Implementación sensor PIR
│   ├── relay/
│   │   ├── relay.h              # Interfaz control relé
│   │   └── relay.cpp            # Implementación relé
│   ├── events/
│   │   ├── event.h              # Definición eventos
│   │   ├── event_manager.h      # Gestor eventos (singleton)
│   │   └── event_manager.cpp    # Implementación event manager
│   └── tasks/
│       ├── wifi_task.h/.cpp     # Tarea WiFi
│       ├── mqtt_task.h/.cpp     # Tarea MQTT
│       └── sensor_task.h/.cpp   # Tarea lectura sensores
├── src/
│   └── main.cpp                 # Punto de entrada
├── platformio.ini               # Configuración build
└── README.md                    # Este archivo
```

## 🚀 Inicio Rápido

### Requisitos

- **PlatformIO** (CLI o VS Code extension)
- **ESP32 NodeMCU-32S** (o compatible)
- **MQTT Broker** (ej: test.mosquitto.org)
- **WiFi** disponible

### Instalación

1. **Clonar el repositorio**
```bash
git clone <repository-url>
cd Electronica\ Info
```

2. **Configurar credenciales WiFi y MQTT**

Editar `include/config/config.h`:
```cpp
static constexpr const char* WIFI_SSID = "Tu_SSID";
static constexpr const char* WIFI_PASSWORD = "Tu_Password";
static constexpr const char* MQTT_SERVER = "tu_broker.mosquitto.org";
```

3. **Compilar y subir**
```bash
platformio run -t upload
```

4. **Monitor serial**
```bash
platformio run -t monitor
```

## 📨 Protocolo MQTT

### Topics Disponibles

**Suscripto:**
- `/actions/relay` - Comandos para el relé
- `/actions/#` - Cualquier acción wildcard

**Ejemplo de Publicación:**
```bash
# Conmutar relé
mosquitto_pub -h test.mosquitto.org -t /actions/relay -m "toggle"
```

### Payloads Soportados

| Topic | Payload | Función |
|-------|---------|---------|
| `/actions/relay` | (cualquiera) | Conmuta el relé (ON ↔ OFF) |

## 🎯 Flujo de Ejecución

```
1. setup()
   ├─ Inicializar Serial
   ├─ Inicializar Sensor PIR
   ├─ Inicializar Relé
   ├─ Registrar listeners en EventManager
   └─ Crear tareas RTOS

2. WiFi Task (Prioridad 1)
   ├─ Conectar a WiFi
   ├─ Mostrar IP local
   └─ Terminar (ejecuta una sola vez)

3. MQTT Task (Prioridad 1)
   ├─ Esperar WiFi conectado
   ├─ Conectar a broker MQTT
   ├─ Suscribirse a /actions/#
   └─ Loop: mantener conexión y procesar mensajes

4. Sensor Task (Prioridad 2)
   ├─ Leer continuamente PIR
   ├─ Mostrar estado cada 2 segundos
   └─ Loop infinito

5. loop()
   └─ Mínimo (RTOS maneja todo)
```

## 🎮 Uso del Sistema

### Conmutar Relé vía MQTT

**Desde terminal:**
```bash
mosquitto_pub -h test.mosquitto.org -t /actions/relay -m "toggle"
```

**Desde Python:**
```python
import paho.mqtt.client as mqtt

client = mqtt.Client()
client.connect("test.mosquitto.org", 1883)
client.publish("/actions/relay", "toggle")
```

**Desde Node.js:**
```javascript
const mqtt = require('mqtt');
const client = mqtt.connect('mqtt://test.mosquitto.org');

client.publish('/actions/relay', 'toggle');
```

### Monitorear en tiempo real

```bash
mosquitto_sub -h test.mosquitto.org -t "/actions/#" -v
```

## 🔧 Patrones y Convenciones

### 1. **Namespaces**
Todo el código está organizado en namespaces para claridad:
```cpp
sensors::PIRSensor
relay::Relay
events::EventManager
events::EventType
tasks::createWiFiTask()
```

### 2. **Event-Driven Architecture**

**Registrar listener:**
```cpp
events::EventManager::getInstance().subscribe(
    events::EventType::RELAY_TOGGLE,
    [](const events::Event& event) {
        relayDevice.toggle();
        relayDevice.printStatus();
    }
);
```

**Disparar evento:**
```cpp
events::EventManager::getInstance().emit(
    events::EventType::RELAY_TOGGLE,
    "relay",
    "toggle_payload"
);
```

### 3. **RTOS Task Management**

Todas las tareas usan funciones factory:
```cpp
tasks::createWiFiTask(priority, handle);
tasks::createMQTTTask(wifiClient, priority, handle);
tasks::createSensorTask(sensor, priority, handle);
```

### 4. **Configuración Centralizada**

Todos los parámetros en `include/config/config.h`:
```cpp
// WiFi
static constexpr const char* WIFI_SSID = "...";

// MQTT
static constexpr const char* MQTT_SERVER = "...";

// Hardware
static constexpr int PIR_SENSOR_PIN = 5;
static constexpr int RELAY_PIN = 27;

// RTOS
static constexpr int WIFI_TASK_PRIORITY = 1;
static constexpr int SENSOR_TASK_PRIORITY = 2;
```

## 📚 API Reference

### Sensor (HC-SR501)

```cpp
sensors::PIRSensor sensor(GPIO_PIN);

sensor.init();                    // Inicializar
bool detected = sensor.isMotionDetected();  // Leer estado
bool last = sensor.getLastState();          // Último estado
sensor.printStatus();             // Imprimir stats
```

### Relé

```cpp
relay::Relay relay(GPIO_PIN);

relay.init();                     // Inicializar
relay.on();                       // Encender
relay.off();                      // Apagar
relay.toggle();                   // Conmutar
bool state = relay.getState();    // Obtener estado
relay.printStatus();              // Imprimir stats
```

### Event Manager

```cpp
events::EventManager& em = events::EventManager::getInstance();

// Registrar listener
em.subscribe(events::EventType::RELAY_TOGGLE, callback);

// Disparar evento
em.emit(events::EventType::RELAY_TOGGLE, "relay", "payload");

// Información
em.printStatus();
em.clear();  // Limpiar todos los listeners
```

## 📝 Agregar Nuevos Sensores

### 1. Crear el sensor

**lib/sensors/nuevo_sensor.h:**
```cpp
namespace sensors {
class NuevoSensor {
private:
    int pin;
public:
    NuevoSensor(int pin);
    void init();
    float read();
};
}
```

**lib/sensors/nuevo_sensor.cpp:**
```cpp
#include "nuevo_sensor.h"

namespace sensors {
NuevoSensor::NuevoSensor(int pin) : pin(pin) {}

void NuevoSensor::init() {
    pinMode(pin, INPUT);
}

float NuevoSensor::read() {
    return analogRead(pin) * 3.3 / 4095.0;
}
}
```

### 2. Crear la tarea (si es necesario)

**lib/tasks/nuevo_sensor_task.h:**
```cpp
namespace tasks {
void createNuevoSensorTask(sensors::NuevoSensor& sensor, 
                           UBaseType_t priority, 
                           TaskHandle_t& handle);
}
```

### 3. Integrar en main.cpp

```cpp
#include <nuevo_sensor.h>
#include <nuevo_sensor_task.h>

sensors::NuevoSensor sensor(PIN);

void setup() {
    sensor.init();
    tasks::createNuevoSensorTask(sensor, priority, handle);
}
```

### 4. Agregar en config.h

```cpp
static constexpr int NUEVO_SENSOR_PIN = 14;
```

## 🔗 Agregar Nuevas Acciones MQTT

### 1. Crear tipo de evento

En `lib/events/event.h`:
```cpp
enum class EventType {
    RELAY_TOGGLE,
    NUEVO_EVENTO,  // ← Agregar
    CUSTOM
};
```

### 2. Registrar listener en main.cpp

```cpp
events::EventManager::getInstance().subscribe(
    events::EventType::NUEVO_EVENTO,
    [](const events::Event& event) {
        // Manejar evento
    }
);
```

### 3. Disparar desde MQTT

En `lib/tasks/mqtt_task.cpp`, en `onMqttMessage()`:
```cpp
if (actionName == "nueva_accion") {
    events::EventManager::getInstance().emit(
        events::EventType::NUEVO_EVENTO,
        actionName.c_str(),
        payloadStr
    );
}
```

## ⚙️ Configuración RTOS

Ajustar prioridades y stack sizes en `include/config/config.h`:

```cpp
// Prioridades (mayor número = más prioridad)
static constexpr int WIFI_TASK_PRIORITY = 1;
static constexpr int MQTT_TASK_PRIORITY = 1;
static constexpr int SENSOR_TASK_PRIORITY = 2;  // ← Sensor con más prioridad

// Stack sizes en bytes
static constexpr int WIFI_TASK_STACK_SIZE = 4096;
static constexpr int MQTT_TASK_STACK_SIZE = 4096;
static constexpr int SENSOR_TASK_STACK_SIZE = 2048;
```

## 🐛 Troubleshooting

### WiFi no conecta
- Verificar SSID/password en `config.h`
- Comprobar que el WiFi está disponible
- Ver output del Serial Monitor

### MQTT no conecta
- Verificar que WiFi está conectado primero
- Comprobar IP/puerto del broker en `config.h`
- Ver estado en Serial Monitor

### Sensor no detecta movimiento
- Esperar ~60 segundos después de encender (estabilización)
- Verificar pin GPIO5 en `config.h`
- Hacer debug: `Serial.println(digitalRead(5))`

### Error de compilación en includes
- Verificar que `build_flags` en `platformio.ini` incluye todas las rutas
- Hacer clean: `platformio run --target clean`

## 📊 Monitoreo y Debug

### Ver logs en tiempo real

```bash
platformio run -t monitor -b 115200
```

### Esperado en el Serial Monitor

```
[Main] Iniciando sistema...
[Sensor] Sensor HC-SR501 inicializado en pin: 5
[Relay] Inicializado en pin: 27
[WiFi] Conectando a WiFi...
[WiFi] ✓ Conectado
[WiFi] IP: 192.168.x.x
[MQTT] Servidor configurado
[MQTT] Intentando conectar...
[MQTT] ✓ Conectado
[MQTT] ✓ Suscrito a /actions/#
[Sensor] Estado PIR: SIN MOVIMIENTO | Último cambio hace: 2000 ms
```

## 🚀 Optimizaciones Aplicadas

✅ **Tareas RTOS** - Paralelismo sin bloqueos  
✅ **Event-Driven** - Bajo acoplamiento entre componentes  
✅ **Static Inline Constexpr** - Sin overhead de memoria global  
✅ **Callbacks Lambda** - Listeners livianos y eficientes  
✅ **Configuración Centralizada** - Fácil ajuste sin recompilación  

## 📄 Licencia

MIT License - Siéntete libre de usar, modificar y distribuir

## 🤝 Contribuciones

Las contribuciones son bienvenidas. Por favor:
1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## 📞 Soporte

Para reportar bugs o sugerir mejoras, abre un **Issue** en el repositorio.

## 🎓 Aprender Más

- [PlatformIO Documentation](https://docs.platformio.org/)
- [ESP32 Arduino Core](https://github.com/espressif/arduino-esp32)
- [FreeRTOS ESP32](https://docs.espressif.com/projects/esp-idf/en/stable/esp32/api-reference/system/freertos.html)
- [MQTT Essentials](https://www.hivemq.com/mqtt-essentials/)
- [PubSubClient Library](https://github.com/knolleary/pubsubclient)

---

**Hecho con ❤️ para IoT**
