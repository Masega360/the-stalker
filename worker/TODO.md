# TODO — The Stalker Worker

## Stats cenitales (YOLO — derivadas de bounding boxes)

- [ ] `crowd_density` — personas / área del frame. Detecta zonas saturadas.
- [ ] `group_count` — cantidad de clusters de personas (distancia entre bounding boxes).
- [ ] `avg_group_size` — tamaño promedio de cada cluster.
- [ ] `dwell_zones` — grilla del frame dividida en celdas, conteo de personas por zona.

> `people_count` ya implementado en `stats/people_stat.py`.

---

## Stats frontales (Rekognition — requiere cámara secundaria a altura de cara)

- [ ] `attention_score` — % de caras mirando hacia la cámara (yaw angle de Rekognition).
- [ ] `smile_rate` — % de personas sonriendo (proxy de satisfacción del cliente).

> `age_mean`, `gender_distribution`, `emotion_dominant` ya implementados en `stats/`.

---

## Infraestructura

- [ ] Definir cómo se combinan stats de cámara cenital y frontal en Nuxt (mismo snapshot o separados por device_id).
- [ ] Configurar segundo ESP32 con cámara frontal.
- [ ] Modo `collect`: recolectar frames del shopping para dataset de entrenamiento futuro.
