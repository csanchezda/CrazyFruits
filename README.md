# Crazy Fruits 🍉🍌🍓

**Crazy Fruits** es un juego interactivo donde debes atrapar frutas con tu boca usando la cámara de tu computadora. Evita las bombas, gana vidas y apunta al TOP 5 de jugadores.

El juego combina **OpenCV** para detección de rostro y boca, **pygame** para sonidos, y un sistema visual de frutas y partículas que hace que la experiencia sea dinámica y entretenida.

> ⚠️ Nota: Solo usar OpenCV dificultaría la integración de música y efectos de sonido, por eso se utiliza **pygame** para manejar audio y HUD.


---

## 🎮 Cómo jugar

1. Colócate frente a la cámara.
2. Escribe tu nombre en el menú principal.
3. Pulsa **JUGAR** para iniciar.
4. Abre la boca para atrapar frutas que caen del cielo.
5. Evita las bombas y captura las frutas especiales que te dan vidas extra.
6. Si pierdes todas tus vidas, el juego termina y se muestra tu puntaje final junto con el **TOP 5** de jugadores.

---

## 🖥️ Funcionalidades principales

### Detección de rostro y boca

* El juego usa **Haar cascades de OpenCV** para detectar tu rostro y la posición de la boca.
* Para mayor precisión, implementamos un **promedio de apertura de boca**.
  Esto significa que no se considera la boca abierta en un solo frame, sino cuando la mayoría de los últimos frames indican que está abierta.

> Esto asegura que abrir la boca de forma breve o accidental no genere errores de detección.

```python
def boca_abierta_promediada(self, is_open):
    self.mouth_states.append(is_open)
    if len(self.mouth_states) > BUFFER_SIZE:
        self.mouth_states.pop(0)
    return sum(self.mouth_states) > BUFFER_SIZE // 2
```

* `BUFFER_SIZE` define cuántos frames se consideran para promediar.
* Esto evita detecciones falsas por movimientos rápidos y hace el juego más fluido.

* Se calcula un **promedio de apertura de boca** durante varios frames.
* Solo si el promedio supera un umbral, se considera que la boca está abierta.
* Esto evita falsos positivos por movimientos rápidos o ruido de la detección.

**Resumen del proceso:**

1. Detectar la cara y la boca.
2. Medir la apertura de la boca (distancia vertical entre puntos clave).
3. Mantener un buffer de aperturas recientes y calcular el promedio.
4. Si el promedio supera un umbral definido (`self.umbral_boca`), se activa la acción de comer fruta.

### Frutas y dificultad

* Diferentes tipos de frutas, cada una con tamaño, velocidad y puntaje propio.
* Frutas especiales:

  * **Mix**: te da una vida extra.
  * **Bomb**: te quita una vida.
* La dificultad aumenta con el tiempo:

  * La velocidad de caída de las frutas aumenta.
  * Se generan frutas con mayor frecuencia.

### Sistema de vidas

* Cada jugador empieza con **6 vidas**.
* Animaciones visuales muestran:

  * **Corazones que laten** al perder vida.
  * **Explosión de partículas** al ganar vida.

### Puntajes y TOP 5

* Los puntajes se guardan automáticamente en `scores.json`.
* Se muestran los 5 mejores jugadores al terminar la partida.

### Sonidos

* Música de fondo en loop.
* Sonidos al:

  * Comer frutas.
  * Perder vida.
  * Ganar vida.
  * Game Over.
* Botón para activar/desactivar sonido.

---

## 🛠️ Requisitos

- Python 3.10 o superior (se recomienda usar un entorno virtual)
- Paquetes Python:
  - `opencv-python`
  - `numpy`
  - `pygame`


```bash
pip install opencv-python numpy pygame
```

- Cámara conectada al computador.

---

## 🛠 Instalación (Windows - PowerShell)

1. Clonar el repositorio:

```powershell
git clone <url-del-repo>
cd CrazyFruits
````

2. (Opcional) Crear y activar un entorno virtual:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

3. Instalar dependencias:

```powershell
pip install opencv-python numpy pygame
# o, si existe requirements.txt:
pip install -r requirements.txt
```

4. Comprobar que la cámara funciona antes de ejecutar el juego.

---

## ▶️ Ejecutar el juego

Desde la carpeta `src`:

```powershell
cd src
python main.py
```

---


## 🏗️ Estructura del proyecto

```
CrazyFruits/
│
├─ assets/               # Imágenes y sonidos
│  ├─ icons/             # Frutas, corazones, íconos de sonido
│  └─ music/             # Música y efectos de sonido
│
├─ src/                  # Código fuente
│  ├─ camera_utils.py
│  ├─ detectors.py
│  ├─ fruta.py
│  ├─ graphics.py
│  ├─ game.py
│  ├─ particulas.py
│  ├─ score_manager.py
│  ├─ tipo_fruta.py
│  ├─ vida.py
│  ├─ sound_manager.py
│  └─ main.py
│
└─ scores.json           # Puntajes guardados
```

---

## 📌 Notas

* El juego usa **OpenCV** para mostrar los frames en tiempo real y detectar tu rostro.
* La lógica de **promediar apertura de boca** evita que el juego reaccione a movimientos pequeños o falsos positivos.
* Puedes salir del juego en cualquier momento pulsando **Q**.


## Solución de problemas comunes

| Problema                              | Solución                                                                                                         |
| ------------------------------------- | ---------------------------------------------------------------------------------------------------------------- |
| "No se pudo abrir la cámara"          | Asegúrate de que otra app no la esté usando. Cambia el índice en `camera_utils.inicializar_camara(cam_index=1)`. |
| Error al cargar cascades              | Verifica que `haarcascade_mcs_mouth.xml` esté presente en `src/`.                                                |
| Imágenes faltantes de frutas o iconos | Revisa `assets/icons/frutas` y `assets/icons`.                                                                   |
| Música no se reproduce                | Confirma que `pygame.mixer` está inicializado y los archivos de `assets/music/` existen.                         |

---

## Créditos

* **Python**: lenguaje base del juego.
* **OpenCV**: detección de cara y boca.
* **pygame**: música, efectos y HUD.
* Iconos y música de `assets/` (propios o libres de uso).



