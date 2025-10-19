# CrazyFruits

CrazyFruits es un juego interactivo en Python donde el jugador debe atrapar frutas con la boca usando la cámara. El juego detecta la cara y la apertura de la boca, generando frutas que caen desde la parte superior de la pantalla. El jugador gana puntos atrapando frutas y pierde vidas si no logra atraparlas.

---

## 🎮 Características

- Detección de **cara** y **boca** mediante cascades de OpenCV.
- Generación de **frutas aleatorias** con diferentes puntuaciones.
- Sistema de **vidas** y **game over**.
- **Partículas** al atrapar frutas.
- Menú interactivo para **Jugar** o **Salir**.
- Pantalla de **Game Over** con opción de volver al menú.
- Todo el juego funciona en tiempo real con la cámara web.


## ⚙ Requisitos

- Python 3.10 o superior
- OpenCV
- NumPy

## 🚀 Cómo ejecutar

1.  **Conecta** tu cámara web.
2.  **Navega** a la carpeta `src/`.
3.  **Ejecuta**:
    ```bash
    python main.py
    ```
4.  En el menú, haz clic en **JUGAR** para empezar.
5.  **Atrapa** las frutas **abriendo la boca**.
6.  Si pierdes todas las vidas, aparecerá la pantalla de **Game Over**.
7.  Haz clic en la pantalla de Game Over para volver al menú.
8.  Presiona **q** en cualquier momento para salir.

-----

## 🕹 Controles

  * **Mouse**: seleccionar opciones en el menú o Game Over.
  * **Boca**: atrapar frutas en la pantalla.
  * **Tecla q**: salir del juego.

-----

## 🛠 Detalles técnicos

El juego utiliza **OpenCV** para:

  * **Detectar** la cara y la boca en tiempo real.
  * **Dibujar** frutas, partículas, vidas y menús.

**Clases principales**:

  * `CrazyFruitsGame`: controla la lógica de juego.
  * `Fruta`: representa una fruta individual.
  * `Particula`: efecto visual al atrapar frutas.
  * `Vida`: controla las vidas del jugador.

**UI** separada en módulos: **menú** y **game over**.

Sistema de **promedio de apertura de boca** para suavizar detecciones.

-----

## 📌 Notas

  * Asegúrate de tener **buena iluminación** para que la detección de la cara y la boca funcione correctamente.
  * El juego está diseñado para funcionar con **una sola persona** frente a la cámara.
  * Puedes modificar la dificultad ajustando la **velocidad** y **frecuencia de generación de frutas** en `game.py`.