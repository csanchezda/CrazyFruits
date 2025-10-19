import cv2
from camera_utils import inicializar_camara
from detectors import cargar_cascades, detectar_boca
from draw_utils import dibujar_cesta, dibujar_face
from fruta import Fruta, generar_fruta, fruta_atrapada

BUFFER_SIZE = 5  # número de frames para promediar

# Parámetros de juego
basket_width = 120
basket_y_offset = 60
dificultad = 1  # puede ir aumentando con el tiempo
frame_counter = 0
generar_cada = 50  # cada cuántos frames generar una fruta

# Lista de frutas
frutas = []

def procesar_cara_y_cesta(frame, face_cascade, smooth_x, alpha):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    frame_height, frame_width = frame.shape[:2]

    faces = face_cascade.detectMultiScale(gray, 1.3, 5)

    if len(faces) > 0:
        x, y, w, h = faces[0]
        face_center_x = dibujar_face(frame, x, y, w, h)

        target_x = int(face_center_x / frame_width * (frame_width - basket_width))
        smooth_x = target_x if smooth_x is None else int(smooth_x * (1 - alpha) + target_x * alpha)
        basket_y = frame_height - basket_y_offset
        dibujar_cesta(frame, smooth_x, basket_y)

        face_roi_gray = gray[y + int(h*0.55):y + h, x:x + w]
        return frame, smooth_x, face_roi_gray, basket_y
    else:
        cv2.putText(frame, "Cara no detectada", (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
        basket_y = frame_height - basket_y_offset
        return frame, smooth_x, None, basket_y

def boca_abierta_promediada(is_open, mouth_states, buffer_size=BUFFER_SIZE):
    mouth_states.append(is_open)
    if len(mouth_states) > buffer_size:
        mouth_states.pop(0)
    return sum(mouth_states) > buffer_size // 2

def procesar_boca_y_texto(frame, boca_abierta):
    if boca_abierta:
        cv2.putText(frame, "Boca abierta!", (20, 80), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)
    else:
        cv2.putText(frame, "Boca cerrada", (20, 80), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (200, 200, 200), 2)
    return frame

def procesar_frame(frame, face_cascade, mouth_cascade, smooth_x, alpha, mouth_states, score):
    global frame_counter, frutas
    frame = cv2.flip(frame, 1)
    frame, smooth_x, face_roi_gray, basket_y = procesar_cara_y_cesta(frame, face_cascade, smooth_x, alpha)

    # Detección de boca con suavizado
    if face_roi_gray is not None:
        is_open = detectar_boca(face_roi_gray, mouth_cascade)
        boca_abierta = boca_abierta_promediada(is_open, mouth_states)
        frame = procesar_boca_y_texto(frame, boca_abierta)
    else:
        boca_abierta = False

    # Generar frutas cada ciertos frames
    frame_counter += 1
    if frame_counter % generar_cada == 0:
        frutas.append(generar_fruta(frame.shape[1], dificultad))

    # Mover y dibujar frutas
    for fruta in frutas:
        fruta.mover()
        fruta.dibujar(frame)

    # Comprobar frutas atrapadas o fuera de pantalla
    nuevas_frutas = []
    for fruta in frutas:
        if fruta_atrapada(fruta, smooth_x, basket_y, basket_width, boca_abierta):
            score[0] += fruta.puntaje  # sumar puntos
        elif fruta.fuera_de_pantalla(frame.shape[0]):
            continue  # se elimina la fruta
        else:
            nuevas_frutas.append(fruta)
    frutas = nuevas_frutas

    # Mostrar puntaje
    cv2.putText(frame, f"Puntaje: {score[0]}", (20, 120), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

    return frame, smooth_x

def main():
    face_cascade, mouth_cascade = cargar_cascades()
    cap = inicializar_camara()
    smooth_x = None
    alpha = 0.2
    mouth_states = []
    score = [0]  # lista para poder pasar como referencia

    print("Presiona 'q' para salir.")
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        frame, smooth_x = procesar_frame(frame, face_cascade, mouth_cascade, smooth_x, alpha, mouth_states, score)
        cv2.imshow("CrazyBasket - Fase 1", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
