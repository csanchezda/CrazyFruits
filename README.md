# 🍉 Crazy Fruits 🍌

> Un juego interactivo donde debes atrapar frutas con tu boca usando la cámara de tu computadora. ¡Evita las bombas, gana vidas y alcanza el TOP 5!

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10+-blue.svg" alt="Python">
  <img src="https://img.shields.io/badge/OpenCV-4.x-green.svg" alt="OpenCV">
  <img src="https://img.shields.io/badge/Pygame-2.x-orange.svg" alt="Pygame">
</p>

---

## 📋 Índice

- [Características](#-características)
- [Cómo jugar](#-cómo-jugar)
- [Requisitos](#-requisitos)
- [Instalación](#-instalación)
- [Ejecutar el juego](#-ejecutar-el-juego)
- [Estructura del proyecto](#-estructura-del-proyecto)
- [Arquitectura técnica](#-arquitectura-técnica)
- [Solución de problemas](#-solución-de-problemas)
- [Créditos](#-créditos)

---

## ✨ Características

### 🎯 Mecánicas de juego
- **Detección facial en tiempo real** usando OpenCV Haar Cascades
- **Sistema de apertura de boca promediado** para evitar falsos positivos
- **Múltiples tipos de frutas** con diferentes velocidades, tamaños y puntajes
- **Frutas especiales**:
  - 🍹 **Mix**: otorga una vida extra
  - 💣 **Bomba**: resta una vida
- **Dificultad progresiva**: las frutas caen más rápido con el tiempo
- **Sistema de vidas** con 6 corazones iniciales

### 🎨 Elementos visuales
- Animaciones de corazones latiendo al perder vida
- Explosión de partículas al ganar vida
- Interfaz gráfica intuitiva con pygame
- HUD con información de puntaje y vidas en tiempo real

### 🔊 Audio
- Música de fondo en loop
- Efectos de sonido para cada acción:
  - Comer frutas 🍓
  - Perder vida 💔
  - Ganar vida ❤️
  - Game Over ☠️
- Botón para activar/desactivar el sonido

### 🏆 Sistema de puntuación
- Guardado automático de puntajes en `scores.json`
- Tabla de **TOP 5** jugadores
- Historial persistente entre sesiones

---

## 🎮 Cómo jugar

1. **Posiciónate** frente a la cámara
2. **Ingresa tu nombre** en el menú principal
3. **Presiona JUGAR** para comenzar
4. **Abre la boca** para atrapar las frutas que caen
5. **Evita las bombas** 💣 y captura frutas especiales para vidas extra
6. **Compite** por el TOP 5 de mejores puntajes

> 💡 **Consejo**: El juego usa un sistema de promedio, así que mantén la boca abierta durante un momento para capturar las frutas.

---

## 📦 Requisitos

### Software
- **Python** 3.10 o superior
- **Cámara web** conectada y funcional

### Dependencias
```bash
opencv-python    # Detección facial, procesamiento de video y interfaz gráfica
numpy           # Operaciones matemáticas
pygame          # Audio
```

---

## 🛠 Instalación

### Windows (PowerShell)

1. **Clonar el repositorio**
```powershell
git clone <url-del-repo>
cd CrazyFruits
```

2. **Crear entorno virtual** (recomendado)
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

3. **Instalar dependencias**
```powershell
pip install opencv-python numpy pygame
```


4. **Verificar la cámara** antes de ejecutar el juego

---

## ▶️ Ejecutar el juego

```powershell
cd src
python main.py
```

Para salir del juego en cualquier momento, presiona **Q**.

---

## 📁 Estructura del proyecto

```
CrazyFruits/
│
├── 📂 assets/                  # Recursos multimedia
│   ├── 📂 icons/               # Imágenes de frutas, corazones, UI
│   │   └── 📂 frutas/          # Sprites de frutas individuales
│   └── 📂 music/               # Música de fondo y efectos de sonido
│
├── 📂 src/                     # Código fuente
│   ├── 📄 main.py              # Punto de entrada principal
│   ├── 📄 camera_utils.py      # Utilidades de cámara
│   ├── 📄 detectors.py         # Detectores de rostro y boca
│   ├── 📄 fruta.py             # Clase Fruta
│   ├── 📄 tipo_fruta.py        # Enum de tipos de fruta
│   ├── 📄 graphics.py          # Renderizado gráfico
│   ├── 📄 game.py              # Lógica principal del juego
│   ├── 📄 particulas.py        # Sistema de partículas
│   ├── 📄 score_manager.py     # Gestión de puntajes
│   ├── 📄 vida.py              # Sistema de vidas
│   └── 📄 sound_manager.py     # Gestión de audio
│
└── 📄 scores.json              # Puntajes guardados (generado)
```

### 📝 Descripción de archivos principales

| Archivo | Descripción |
|---------|-------------|
| `main.py` | Inicializa el juego, carga recursos y ejecuta el bucle principal |
| `camera_utils.py` | Funciones para inicializar y gestionar la cámara web |
| `detectors.py` | Implementa la detección de rostro y boca con OpenCV Haar Cascades |
| `fruta.py` | Define la clase Fruta con física de caída y detección de colisión |
| `tipo_fruta.py` | Enum con todos los tipos de frutas y sus propiedades (puntos, velocidad, tamaño) |
| `graphics.py` | Maneja todo el renderizado visual: HUD, menús, partículas y efectos |
| `game.py` | Contiene la lógica central del juego: generación de frutas, manejo de colisiones y estados |
| `particulas.py` | Sistema de partículas para efectos visuales al ganar/perder vidas |
| `score_manager.py` | Gestiona la persistencia de puntajes en JSON y el ranking TOP 5 |
| `vida.py` | Controla el sistema de vidas con animaciones de corazones |
| `sound_manager.py` | Administra música de fondo y efectos de sonido con pygame.mixer |

---

## 🔧 Arquitectura técnica

### Sistema de detección de boca promediado

El juego implementa un **algoritmo de promedio de apertura de boca** para mayor precisión:

```python
def boca_abierta_promediada(self, is_open):
    self.mouth_states.append(is_open)
    if len(self.mouth_states) > BUFFER_SIZE:
        self.mouth_states.pop(0)
    return sum(self.mouth_states) > BUFFER_SIZE // 2
```

**¿Cómo funciona?**

1. 📸 Detecta la cara y la boca en cada frame
2. 📏 Mide la apertura vertical de la boca
3. 📊 Mantiene un buffer de las últimas mediciones
4. ✅ Solo activa la acción si el promedio supera el umbral

**Ventajas:**
- ✨ Evita falsos positivos por movimientos rápidos
- 🎯 Mayor precisión en la detección
- 🎮 Experiencia de juego más fluida

> ⚠️ **Nota**: Se usa pygame junto con OpenCV porque OpenCV por sí solo dificulta la integración de música y efectos de sonido de forma eficiente.

### Dificultad progresiva

- ⚡ **Velocidad**: Aumenta gradualmente con el tiempo de juego
- 🔄 **Frecuencia**: Generación más rápida de frutas
- 🎯 **Variedad**: Mayor probabilidad de frutas especiales en niveles avanzados

---

## 🐛 Solución de problemas

| Problema | Solución |
|----------|----------|
| ❌ "No se pudo abrir la cámara" | • Verifica que ninguna otra aplicación esté usando la cámara<br>• Intenta cambiar el índice: `inicializar_camara(cam_index=1)` |
| ❌ Error al cargar cascades | • Confirma que `haarcascade_mcs_mouth.xml` existe en `src/`<br>• Verifica los permisos de lectura del archivo |
| ❌ Imágenes faltantes | • Revisa que `assets/icons/frutas/` contenga todas las imágenes<br>• Verifica la estructura de carpetas |
| ❌ Sin sonido | • Confirma que `pygame.mixer` está inicializado<br>• Verifica que los archivos en `assets/music/` existen<br>• Revisa el volumen del sistema |
| ❌ Detección imprecisa | • Mejora la iluminación de tu entorno<br>• Ajusta la distancia a la cámara<br>• Modifica `BUFFER_SIZE` para cambiar la sensibilidad |

---

## 🎖️ Créditos

- **Lenguaje**: Python 3.10+
- **Visión por computadora**: OpenCV
- **Motor de juego**: Pygame
- **Recursos multimedia**: Assets de uso libre

---

<p align="center">
  Hecho con ❤️ y muchas 🍓🍌🍉
</p>

<p align="center">
  ¿Encontraste un bug? ¿Tienes una sugerencia? ¡Abre un issue!
</p>