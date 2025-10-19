# graphics.py
import cv2

# -------------------------------
# Dibujo de cara y boca
# -------------------------------
def dibujar_face(frame, x, y, w, h):
    """
    Dibuja un rectángulo y línea central sobre la cara detectada.
    Devuelve el centro X de la cara.
    """
    face_center_x = x + w // 2
    cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 150, 0), 2)
    cv2.line(frame, (face_center_x, 0), (face_center_x, frame.shape[0]), (0, 255, 255), 1)
    return face_center_x

def dibujar_boca(frame, x, y, radio=5, color=(0, 255, 255)):
    """
    Dibuja un punto en la posición de la boca.
    """
    cv2.circle(frame, (x, y), radio, color, -1)

# -------------------------------
# Dibujo de puntaje y vidas
# -------------------------------
def dibujar_puntaje(frame, score, x=20, y=80, color=(0, 255, 0)):
    cv2.putText(frame, f"Puntaje: {score}", (x, y),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, color, 2)

def dibujar_vidas(frame, vidas_actual, vidas_total, x=20, y=20):
    """
    Dibuja corazones pequeños y número de vidas.
    """
    for i in range(vidas_actual):
        cv2.circle(frame, (x + i*30, y), 10, (0, 0, 255), -1)
    cv2.putText(frame, f"{vidas_actual}/{vidas_total}", (x, y + 40),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

# -------------------------------
# Dibujo de menú
# -------------------------------
def dibujar_menu(frame, opciones, menu_rects):
    """
    Dibuja un menú con las opciones pasadas y devuelve los rects de cada opción.
    """
    frame[:] = (50, 50, 50)  # fondo gris
    h, w = frame.shape[:2]
    rects = []

    for i, texto in enumerate(opciones):
        x1, y1 = int(w*0.35), int(h*(0.4 + i*0.2))
        x2, y2 = int(w*0.65), int(h*(0.5 + i*0.2))
        cv2.rectangle(frame, (x1, y1), (x2, y2), (100, 100, 255), -1)
        cv2.putText(frame, texto, (x1 + 20, y1 + 40),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
        rects.append((x1, y1, x2, y2))

    menu_rects.clear()
    menu_rects.extend(rects)
    return frame

# -------------------------------
# Dibujo de frutas
# -------------------------------
FRUTA_COLORES = {
    'manzana': (0, 255, 0),
    'banana': (255, 255, 0),
    'naranja': (0, 165, 255)
}

def dibujar_fruta(frame, fruta):
    color = FRUTA_COLORES.get(fruta.tipo, (255, 255, 255))
    cv2.circle(frame, (fruta.x, fruta.y), fruta.tam // 2, color, -1)

# -------------------------------
# Dibujo de partículas
# -------------------------------
def dibujar_particula(frame, particula):
    if particula.vida > 0:
        cv2.circle(frame, (particula.x, particula.y), 3, particula.color, -1)