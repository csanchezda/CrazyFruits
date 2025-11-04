"""
Funciones y utilidades para dibujar la UI del juego en frames OpenCV.

Este módulo centraliza la lógica de renderizado: menú, HUD (puntaje/vidas),
dibujado de frutas con transparencia, efectos de partículas y animaciones
de corazones.
"""

import cv2
import os
import random
import math
import numpy as np

from fruta import TipoFruta

# -------------------------------


SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
HEART_PATH = os.path.join(SCRIPT_DIR, "../assets/icons/heart.png")
HEART_IMG = cv2.imread(HEART_PATH, cv2.IMREAD_UNCHANGED)
ICON_PATH_ON = os.path.join(SCRIPT_DIR, "../assets/icons/sound_on.png")
ICON_PATH_OFF = os.path.join(SCRIPT_DIR, "../assets/icons/sound_off.png")
ICON_ON = cv2.imread(ICON_PATH_ON, cv2.IMREAD_UNCHANGED)
ICON_OFF = cv2.imread(ICON_PATH_OFF, cv2.IMREAD_UNCHANGED)
FRUIT_BG_PATH = os.path.join(SCRIPT_DIR, "../assets/icons/fruit-background.jpg")

# -------------------------------
# Dibujo de cara y boca
# -------------------------------
def dibujar_face(frame, x, y, w, h):
    """Dibuja un rectángulo sobre la cara y una línea vertical central.

    Devuelve la coordenada X central de la cara (útil para alinear elementos).
    """
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
    """Dibuja un corazón con transparencia.

    Usa una imagen PNG con canal alfa si está disponible, si no se dibuja
    un círculo como fallback para mantener el feedback visual.
    """
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
# Animaciones de corazones
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

def dibujar_animacion_ganar_corazon(frame, x, y, tam=44, frame_idx=0):
    """
    Animación de vida ganada mejorada: latido marcado + explosión de partículas + fade.
    """
    total_frames = 30
    t = frame_idx / total_frames

    # --- Latido del corazón ---
    escala = 1.0 + 0.5 * math.sin(math.pi * t * 2)  # dos pulsos rápidos
    opacidad = 1.0 if t < 0.8 else max(0, 1.0 - (t - 0.8)/0.2)

    # Dibujar el corazón
    if HEART_IMG is None:
        color = (0, int(255 * opacidad), int(100 * opacidad))
        cv2.circle(frame, (x + tam//2, y + tam//2), int(12 * escala), color, -1)
    else:
        h, w = HEART_IMG.shape[:2]
        new_w, new_h = int(w * tam * escala / max(h, w)), int(h * tam * escala / max(h, w))
        heart_scaled = cv2.resize(HEART_IMG, (new_w, new_h), interpolation=cv2.INTER_AREA)

        x1, y1 = x, y
        x2, y2 = x1 + new_w, y1 + new_h
        if x2 <= frame.shape[1] and y2 <= frame.shape[0]:
            heart_crop = heart_scaled[:(y2 - y1), :(x2 - x1)]
            if heart_crop.shape[2] == 4:
                alpha_s = (heart_crop[:, :, 3]/255.0) * opacidad
                alpha_l = 1.0 - alpha_s
                for c in range(3):
                    frame[y1:y2, x1:x2, c] = alpha_s * heart_crop[:, :, c] + alpha_l * frame[y1:y2, x1:x2, c]

    # --- Explosión de partículas alrededor del corazón ---
    num_particulas = 20
    for i in range(num_particulas):
        angle = 2 * math.pi * i / num_particulas + frame_idx * 0.2
        radio_max = tam * (1.5 + t*2)  # partículas se expanden
        dx = int(math.cos(angle) * radio_max)
        dy = int(math.sin(angle) * radio_max)
        intensidad = int(255 * (1 - t))
        color = (intensidad, 255, intensidad)
        cv2.circle(frame, (x + tam//2 + dx, y + tam//2 + dy), 3, color, -1)


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



def dibujar_vidas(frame, vidas_actual, x=30, y=80, animaciones=None, animaciones_ganar=None):
    separacion = 48
    for i in range(vidas_actual):
        dibujar_corazon(frame, x + i * separacion, y, tam=44)

    # Animaciones de pérdida
    if animaciones:
        nuevas_anim = []
        for anim in animaciones:
            idx, f = anim["indice"], anim["frame"]
            dibujar_animacion_corazon(frame, x + idx * separacion, y, tam=44, frame_idx=f)
            if f < 12:
                nuevas_anim.append({"indice": idx, "frame": f + 1})
        animaciones[:] = nuevas_anim

    # Animaciones de vida ganada
    if animaciones_ganar:
        nuevas_anim_ganar = []
        for anim in animaciones_ganar:
            idx, f = anim["indice"], anim["frame"]
            dibujar_animacion_ganar_corazon(frame, x + idx * separacion, y, tam=44, frame_idx=f)
            if f < 20:
                nuevas_anim_ganar.append({"indice": idx, "frame": f + 1})
        animaciones_ganar[:] = nuevas_anim_ganar



# -------------------------------
# Dibujo de menú
# -------------------------------

def dibujar_menu(frame, opciones, menu_rects, nombre_jugador):
    h, w = frame.shape[:2]

    # --- Fondo con imagen ---
    fondo_img = cv2.imread(FRUIT_BG_PATH)
    if fondo_img is not None:
        # Redimensionar al tamaño del frame
        fondo_img = cv2.resize(fondo_img, (w, h))
        frame[:] = fondo_img.copy()
    else:
        # Si falla, dejar degradado pastel como fallback
        fondo = np.zeros_like(frame, dtype=np.uint8)
        for i in range(h):
            r = int(150 + i * 0.05)
            g = int(200 + i * 0.1)
            b = int(255 - i * 0.05)
            cv2.line(fondo, (0, i), (w, i), (b, g, r), 1)
        frame[:] = cv2.addWeighted(fondo, 0.7, frame, 0.3, 0)

    # --- Título ---
    titulo = "CRAZY FRUITS"
    font = cv2.FONT_HERSHEY_DUPLEX
    sombra = (50, 50, 50)
    color_principal = (255, 255, 255)

    (tw, th), _ = cv2.getTextSize(titulo, font, 2, 4)
    cx, cy = (w - tw)//2, int(h*0.25)
    cv2.putText(frame, titulo, (cx + 3, cy + 3), font, 2, sombra, 5, cv2.LINE_AA)
    cv2.putText(frame, titulo, (cx, cy), font, 2, color_principal, 3, cv2.LINE_AA)

    # --- Campo para nombre ---
    campo_w, campo_h = 420, 60
    campo_x = (w - campo_w)//2
    campo_y = int(h*0.45)
    color_campo = (230, 250, 250)
    cv2.rectangle(frame, (campo_x, campo_y), (campo_x + campo_w, campo_y + campo_h), color_campo, -1)
    cv2.rectangle(frame, (campo_x, campo_y), (campo_x + campo_w, campo_y + campo_h), (0, 200, 180), 2)
    texto = nombre_jugador if nombre_jugador else "Escribe tu nombre..."
    color_texto = (60, 60, 60) if nombre_jugador else (160, 160, 160)
    cv2.putText(frame, texto, (campo_x + 15, campo_y + 40), font, 0.9, color_texto, 2, cv2.LINE_AA)
    campo_nombre_rect = (campo_x, campo_y, campo_x + campo_w, campo_y + campo_h)

    # --- Botones ---
    btn_w, btn_h = 300, 70
    start_y = int(h * 0.62)
    espacio = 90
    menu_rects.clear()

    for i, texto_btn in enumerate(opciones):
        bx = (w - btn_w)//2
        by = start_y + i * espacio
        rect = (bx, by, bx + btn_w, by + btn_h)
        menu_rects.append(rect)

        color_btn = (255, 255, 255)
        borde = (0, 255, 220)
        cv2.rectangle(frame, (bx, by), (bx + btn_w, by + btn_h), color_btn, -1)
        cv2.rectangle(frame, (bx, by), (bx + btn_w, by + btn_h), borde, 3)

        (tw, th), _ = cv2.getTextSize(texto_btn, font, 1.1, 3)
        tx = bx + (btn_w - tw)//2
        ty = by + (btn_h + th)//2
        cv2.putText(frame, texto_btn, (tx + 2, ty + 2), font, 1.1, sombra, 3, cv2.LINE_AA)
        cv2.putText(frame, texto_btn, (tx, ty), font, 1.1, (0, 150, 130), 2, cv2.LINE_AA)

    # --- Destellos ---
    NUM_DESTELLOS = 20  # ahora habrá más destellos

    if not hasattr(dibujar_menu, "_destellos"):
        # Inicializamos posiciones y velocidades de cada destello
        dibujar_menu._destellos = [
            {"x": random.uniform(0, w), "y": random.uniform(0, h),
            "vx": random.uniform(-1, 1), "vy": random.uniform(-0.5, 0.5),
            "radio": random.randint(2, 4)}  # tamaño aleatorio para más naturalidad
            for _ in range(NUM_DESTELLOS)
        ]

    for d in dibujar_menu._destellos:
        # Mover con velocidad propia
        d["x"] += d["vx"] * 2
        d["y"] += d["vy"] * 2

        # Rebotar si toca bordes
        if d["x"] < 0 or d["x"] >= w:
            d["vx"] *= -1
        if d["y"] < 0 or d["y"] >= h:
            d["vy"] *= -1

        # Dibujar destello
        cx, cy = int(d["x"]), int(d["y"])
        cv2.circle(frame, (cx, cy), d["radio"], (0, 30, 255), -1)
        cv2.circle(frame, (cx, cy), d["radio"]*2, (0, 30, 255), 1)
    return campo_nombre_rect



# -------------------------------
# Icono de sonido
# -------------------------------
def dibujar_icono_sonido(frame, muted, x=20, y=20, tam=40):
    icon = ICON_OFF if muted else ICON_ON
    if icon is None:
        print("Icono de sonido no encontrado, usando texto.")
        cv2.putText(frame, "Mute" if muted else "Sound", (x, y+30),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,255), 2)
        return (x, y, x+tam, y+tam)
    
    icon = cv2.resize(icon, (tam, tam))
    h, w = icon.shape[:2]
    alpha = icon[:, :, 3] / 255.0
    for c in range(3):
        frame[y:y+h, x:x+w, c] = alpha * icon[:, :, c] + (1 - alpha) * frame[y:y+h, x:x+w, c]
    return (x, y, x+tam, y+tam)

# -------------------------------
# Dibujo de frutas
# -------------------------------

# Colores BGR según tipo de fruta
FRUTA_COLORES_BGR = {
    "LEMON": (63, 237, 253),        # RGB(253,237,63)
    "CHERRY": (65, 27, 228),        # RGB(228,27,65)
    "BOMB": (67, 65, 65),           # RGB(65,65,67)
    "BANANA": (94, 238, 252),       # RGB(252,238,94)
    "APPLE": (57, 55, 230),         # RGB(230,55,57)
    "MIX": (171, 201, 224),         # RGB(224,201,171)
    "ORANGE": (86, 160, 245),       # RGB(245,160,86)
    "PEAR": (16, 210, 196),         # RGB(196,210,16)
    "RASPBERRY": (87, 56, 231),     # RGB(231,56,87)
    "STRAWBERRY": (101, 87, 234),   # RGB(234,87,101)
    "WATERMELON": (57, 55, 230)     # RGB(230,55,57)
}


def dibujar_fruta(frame, fruta):
    """Dibuja una fruta usando su imagen PNG con transparencia."""
    if fruta.imagen is not None:
        fh, fw = fruta.imagen.shape[:2]
        x1 = int(fruta.x - fw // 2)
        y1 = int(fruta.y - fh // 2)
        x2 = x1 + fw
        y2 = y1 + fh

        if x1 < 0 or y1 < 0 or x2 > frame.shape[1] or y2 > frame.shape[0]:
            return

        fruta_crop = fruta.imagen[:(y2 - y1), :(x2 - x1)]

        if fruta_crop.shape[2] == 4:
            alpha = fruta_crop[:, :, 3] / 255.0
            for c in range(3):
                frame[y1:y2, x1:x2, c] = (
                    alpha * fruta_crop[:, :, c] +
                    (1 - alpha) * frame[y1:y2, x1:x2, c]
                )
        else:
            frame[y1:y2, x1:x2] = fruta_crop
    else:
        # fallback: círculo si no hay imagen
        color = (255, 255, 255) if fruta.tipo != TipoFruta.BOMB else (0, 0, 0)
        cv2.circle(frame, (int(fruta.x), int(fruta.y)), fruta.tam // 2, color, -1)

# -------------------------------
# Dibujo de partículas
# -------------------------------
def dibujar_particula(frame, particula):
    """Dibuja una partícula si está activa."""
    if particula.vida > 0:
        cv2.circle(frame, (int(particula.x), int(particula.y)), 3, particula.color, -1)