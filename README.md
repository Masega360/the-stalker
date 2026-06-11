# The Stalker

Sistema de análisis de personas en tiempo real usando ESP32, MQTT, AWS Rekognition y Nuxt. Captura imágenes desde cámaras ESP32, detecta personas, analiza emociones, edad y género, y permite actuar relays desde el frontend.

## Arquitectura

```
ESP32 (cámara/actuador)
    ↕ MQTT
Mosquitto Broker
    ↕ MQTT
Python Worker  ←→  Nuxt (Frontend + Backend)
                         ↓
                         DB
```
 
---

## MQTT

### Topics que escucha el worker

| Topic | Dirección | Descripción |
|-------|-----------|-------------|
| `***` | ESP32 → Worker | Imagen de cámara (bytes JPEG) |
| `register/cam` | ESP32 → Worker | Registro de nueva cámara |
| `register/actor` | ESP32 → Worker | Registro de nuevo actuador |

### Topics que publica el worker

| Topic | Dirección | Descripción |
|-------|-----------|-------------|
| `{device_id}/actions/relay` | Worker → ESP32 | Comando para actuar relay |

### Topics que escucha el ESP32

| Topic | Descripción |
|-------|-------------|
| `{device_id}/actions/relay` | Recibe comando de relay |

### Topics que publica el ESP32

| Topic | Descripción |
|-------|-------------|
| `register/cam` | Al conectarse, si es cámara |
| `register/actor` | Al conectarse, si es actuador |
| `{device_id}/sensors/hc-sr501` | Datos del sensor de movimiento |
| `{device_id}/status` | Estado del dispositivo |
| `***` | Frame de imagen (bytes JPEG) |

### Payloads MQTT

**`register/cam` / `register/actor`**
```
TODO
```
Ejemplo: `esp32-cam-01`

**`{device_id}/actions/relay`**
```
TODO
```

**`***`** la ruta de la foto
```
TODO
```

---

## HTTP API (Worker)

Base URL: `http://<worker_host>:<WORKER_PORT>`

Todos los endpoints requieren el header:
```
x-api-key: <INTERNAL_API_KEY>
```

### POST `/relay/{device_id}`

Actúa el relay de un actuador ESP32.

**Request:**
```json
{
  "state": true
}
```
`state: true` = encender, `state: false` = apagar

**Response 200:**
```json
{
  "ok": true,
  "device_id": "esp32-actor-01",
  "state": true
}
```

**Response 401:**
```json
{ "error": "Unauthorized" }
```

**Response 500:**
```json
{ "error": "No se pudo publicar en MQTT" }
```

---

**Tipos de stats generados por snapshot:**

| stat_type | data_type | Descripción |
|-----------|-----------|-------------|
| `people_count` | int | Total de personas detectadas (incluye espaldas) |
| `male_count` | int | Cantidad de caras masculinas |
| `female_count` | int | Cantidad de caras femeninas |
| `age_mean` | float | Edad promedio estimada |
| `age_min` | int | Edad mínima estimada |
| `age_max` | int | Edad máxima estimada |
| `age_std` | float | Desviación estándar de edades |
| `happy_count` | int | Caras con emoción dominante HAPPY |
| `sad_count` | int | Caras con emoción dominante SAD |
| `angry_count` | int | Caras con emoción dominante ANGRY |
| `surprised_count` | int | Caras con emoción dominante SURPRISED |
| `neutral_count` | int | Caras con emoción dominante NEUTRAL |
| `disgusted_count` | int | Caras con emoción dominante DISGUSTED |
| `confused_count` | int | Caras con emoción dominante CONFUSED |
| `calm_count` | int | Caras con emoción dominante CALM |
| `face_N_emotion` | json | Emoción y posición de la cara N |

**Ejemplo de `face_N_emotion`:**
```json
{
  "snapshot_id": "uuid-v4",
  "device_id": "esp32-cam-01",
  "time": "2026-04-23T12:00:00+00:00",
  "stat_type": "face_1_emotion",
  "data_type": "json",
  "value": {
    "emotion": "HAPPY",
    "confidence": 98.5,
    "position": {
      "left": 0.32,
      "top": 0.15
    }
  }
}
```
`position.left` y `position.top` son valores normalizados entre 0 y 1 (0 = borde izquierdo/superior, 1 = borde derecho/inferior).

### POST `/api/internal/devices/register`

El worker notifica el registro de un nuevo dispositivo.

**Body:**
```json
{
  "device_id": "esp32-cam-01",
  "type": "cam"
}
```
`type`: `"cam"` o `"actor"`


## HTTP API (Nuxt — endpoints que consume el worker)