# graphics.py
import cv2
import os
import time
import math

# -------------------------------
# Cargar imagen del corazón
# -------------------------------
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
HEART_PATH = os.path.join(SCRIPT_DIR, "../asserts/heart.png")
HEART_IMG = cv2.imread(HEART_PATH, cv2.IMREAD_UNCHANGED)

# -------------------------------
# Dibujo de cara y boca
# -------------------------------
def dibujar_face(frame, x, y, w, h):
    """Dibuja un rectángulo sobre la cara y una línea vertical central."""
    face_center_x = x + w // 2
    cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 150, 0), 2)
    cv2.line(frame, (face_center_x, 0), (face_center_x, frame.shape[0]), (0, 255, 255), 1)
    return face_center_x


def dibujar_boca(frame, x, y, radio=5, color=(0, 255, 255)):
    """Marca el punto de la boca detectada."""
    cv2.circle(frame, (x, y), radio, color, -1)

# -------------------------------
# Dibujo base del corazón
# -------------------------------
def dibujar_corazon(frame, x, y, tam=42):
    """Dibuja un corazón con transparencia."""
    if HEART_IMG is None:
        cv2.circle(frame, (x + tam // 2, y + tam // 2), 12, (0, 0, 255), -1)
        return

    h, w = HEART_IMG.shape[:2]
    escala = tam / max(h, w)
    new_w, new_h = int(w * escala), int(h * escala)
    heart_resized = cv2.resize(HEART_IMG, (new_w, new_h), interpolation=cv2.INTER_AREA)

    x1, y1 = x, y
    x2, y2 = x1 + new_w, y1 + new_h
    if x1 < 0 or y1 < 0 or x2 > frame.shape[1] or y2 > frame.shape[0]:
        return

    heart_crop = heart_resized[:(y2 - y1), :(x2 - x1)]

    # Combinar con alfa
    if heart_crop.shape[2] == 4:
        alpha_s = heart_crop[:, :, 3] / 255.0
        alpha_l = 1.0 - alpha_s
        for c in range(3):
            frame[y1:y2, x1:x2, c] = (
                alpha_s * heart_crop[:, :, c] +
                alpha_l * frame[y1:y2, x1:x2, c]
            )
    else:
        frame[y1:y2, x1:x2] = heart_crop[:, :, :3]


# -------------------------------
# Animación de pérdida (latido + fade)
# -------------------------------
def dibujar_animacion_corazon(frame, x, y, tam=44, frame_idx=0):
    """
    Animación rápida de pérdida de vida: doble latido ágil + desvanecimiento elegante.
    """
    total_frames = 12  # duración más corta → latido más rápido
    t = frame_idx / total_frames

    # Curva de escala (más rápida y con un segundo pulso corto)
    if t < 0.25:
        escala = 1.0 + 0.3 * (t / 0.25)         # crece rápido
    elif t < 0.45:
        escala = 1.3 - 0.25 * ((t - 0.25) / 0.2) # se encoge un poco
    elif t < 0.65:
        escala = 1.05 + 0.2 * ((t - 0.45) / 0.2) # segundo pulso corto
    else:
        escala = 1.25 + 0.4 * ((t - 0.65) / 0.35) # se expande y desvanece

    # Opacidad: visible casi todo el tiempo, luego se desvanece suave
    opacidad = 1.0 if t < 0.75 else max(0, 1.0 - (t - 0.75) / 0.25)

    # Si no hay imagen, usa un corazón dibujado (fallback)
    if HEART_IMG is None:
        color = (int(255 * opacidad), int(100 + 100 * opacidad), int(180 * opacidad))
        cv2.circle(frame, (x + tam // 2, y + tam // 2), int(12 * escala), color, -1)
        return

    # Escalar y posicionar el corazón
    h, w = HEART_IMG.shape[:2]
    new_w, new_h = int(w * tam * escala / max(h, w)), int(h * tam * escala / max(h, w))
    heart_scaled = cv2.resize(HEART_IMG, (new_w, new_h), interpolation=cv2.INTER_AREA)

    x1, y1 = x, y
    x2, y2 = x1 + new_w, y1 + new_h
    if x2 > frame.shape[1] or y2 > frame.shape[0]:
        return

    heart_crop = heart_scaled[:(y2 - y1), :(x2 - x1)]
    if heart_crop.shape[2] == 4:
        alpha_s = (heart_crop[:, :, 3] / 255.0) * opacidad
        alpha_l = 1.0 - alpha_s
        for c in range(3):
            frame[y1:y2, x1:x2, c] = (
                alpha_s * heart_crop[:, :, c] +
                alpha_l * frame[y1:y2, x1:x2, c]
            )



def dibujar_puntaje(frame, score, x=30, y=60):
    """Texto con sombra, fuente moderna y color suave."""
    sombra_color = (30, 30, 30)
    texto_color = (0, 255, 200)

    cv2.putText(
        frame, f"Puntaje: {score}", (x + 2, y + 2),
        cv2.FONT_HERSHEY_DUPLEX, 0.9, sombra_color, 2, cv2.LINE_AA
    )
    cv2.putText(
        frame, f"Puntaje: {score}", (x, y),
        cv2.FONT_HERSHEY_DUPLEX, 0.9, texto_color, 1, cv2.LINE_AA
    )



def dibujar_vidas(frame, vidas_actual, x=30, y=80, animaciones=None):
    """Dibuja los corazones y maneja las animaciones de pérdida."""
    separacion = 48
    for i in range(vidas_actual):
        dibujar_corazon(frame, x + i * separacion, y, tam=44)

    # Dibujar animaciones activas
    if animaciones:
        nuevas_anim = []
        for anim in animaciones:
            idx, f = anim["indice"], anim["frame"]
            dibujar_animacion_corazon(frame, x + idx * separacion, y, tam=44, frame_idx=f)
            if f < 12:
                nuevas_anim.append({"indice": idx, "frame": f + 1})
        animaciones[:] = nuevas_anim

# -------------------------------
# Dibujo de menú
# -------------------------------
def dibujar_menu(frame, opciones, menu_rects):
    """Dibuja el menú principal con las opciones."""
    frame[:] = (50, 50, 50)  # fondo gris
    h, w = frame.shape[:2]
    rects = []

    for i, texto in enumerate(opciones):
        x1, y1 = int(w * 0.35), int(h * (0.4 + i * 0.2))
        x2, y2 = int(w * 0.65), int(h * (0.5 + i * 0.2))

        cv2.rectangle(frame, (x1, y1), (x2, y2), (100, 100, 255), -1)
        cv2.putText(
            frame,
            texto,
            (x1 + 20, y1 + 40),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (255, 255, 255),
            2
        )
        rects.append((x1, y1, x2, y2))

    menu_rects.clear()
    menu_rects.extend(rects)
    return frame

# -------------------------------
# Dibujo de frutas
# -------------------------------
FRUTA_COLORES = {
    "sandia": (0, 0, 255),     # rojo
    "platano": (0, 255, 255),  # amarillo
    "manzana": (0, 200, 0)     # verde
}


def dibujar_fruta(frame, fruta):
    """Dibuja una fruta con color según su tipo."""
    color = FRUTA_COLORES.get(fruta.tipo, (255, 255, 255))
    cv2.circle(frame, (int(fruta.x), int(fruta.y)), fruta.tam // 2, color, -1)

# -------------------------------
# Dibujo de partículas
# -------------------------------
def dibujar_particula(frame, particula):
    """Dibuja una partícula si está activa."""
    if particula.vida > 0:
        cv2.circle(frame, (int(particula.x), int(particula.y)), 3, particula.color, -1)