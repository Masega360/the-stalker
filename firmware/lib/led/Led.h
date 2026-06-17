#ifndef LEDBUILTIN_H
#define LEDBUILTIN_H

#include <Arduino.h>
#include <Adafruit_NeoPixel.h>

#ifdef DEVICE_ROLE_ACTOR
#define LED_BUILTIN_PIN 2
#define USE_NEOPIXEL
#elif defined(DEVICE_ROLE_CAMERA)
#define LED_BUILTIN_PIN 33 // LED rojo incorporado en la mayoría de ESP32-CAM (activo en BAJO)
#endif

#define LED_POWER 50

namespace Led {

    namespace Colors {
        static const uint8_t RED[] = {255, 0, 0};
        static const uint8_t GREEN[] = {0, 255, 0};
        static const uint8_t BLUE[] = {0, 0, 255};
        static const uint8_t YELLOW[] = {255, 255, 0};
        static const uint8_t CYAN[] = {0, 255, 255};
        static const uint8_t MAGENTA[] = {255, 0, 255};
        static const uint8_t WHITE[] = {255, 255, 255};
        static const uint8_t OFF[] = {0, 0, 0};
    }

    namespace LedBuiltIn
    {
        static void setColor(uint8_t r, uint8_t g, uint8_t b) {
#ifdef USE_NEOPIXEL
            Adafruit_NeoPixel strip(1, LED_BUILTIN_PIN, NEO_GRB + NEO_KHZ800);
            strip.begin();
            strip.setPixelColor(0, strip.Color(r, g, b));
            strip.show();
#else
            // Para ESP32-CAM, el LED suele ser GPIO 33 (rojo) y es Activo Bajo
            // Solo podemos controlar encendido/apagado (usamos R como indicador)
            pinMode(LED_BUILTIN_PIN, OUTPUT);
            if (r > 0 || g > 0 || b > 0) {
                digitalWrite(LED_BUILTIN_PIN, LOW); // ON
            } else {
                digitalWrite(LED_BUILTIN_PIN, HIGH); // OFF
            }
#endif
        }
        
        static void setColor(const uint8_t color[3]) {
            setColor(
                (uint8_t) ((color[0] * LED_POWER) / 100),
                (uint8_t) ((color[1] * LED_POWER) / 100),
                (uint8_t) ((color[2] * LED_POWER) / 100)
            );
        }

        static void setColor(const uint8_t color[3], uint16_t ms) {
            setColor(
                (uint8_t) ((color[0] * LED_POWER) / 100),
                (uint8_t) ((color[1] * LED_POWER) / 100),
                (uint8_t) ((color[2] * LED_POWER) / 100)
            );
            vTaskDelay(ms / portTICK_PERIOD_MS);
            setColor(Colors::OFF);
        }
    }
    
}

#endif // LEDBUILTIN_H