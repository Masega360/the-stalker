#ifndef ESP32_CAM_H
#define ESP32_CAM_H

#include "esp_camera.h"
#include <Arduino.h>

namespace camera {

/**
 * @brief Inicializa el hardware de la cámara ESP32-CAM
 * @return true si la inicialización fue exitosa, false de lo contrario
 */
bool initCamera();

/**
 * @brief Captura una imagen
 * @return Puntero al buffer de la cámara (camera_fb_t*) o nullptr si falló
 */
camera_fb_t* captureFrame();

/**
 * @brief Libera el buffer de la cámara
 * @param fb Puntero al buffer a liberar
 */
void releaseFrame(camera_fb_t* fb);

} // namespace camera

#endif // ESP32_CAM_H
