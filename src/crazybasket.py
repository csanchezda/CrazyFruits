import cv2
from camera_utils import inicializar_camara
from detectors import cargar_cascades, detectar_boca
from fruta import Fruta, generar_fruta, fruta_atrapada_por_boca
from draw_utils import dibujar_face  # solo para dibujar el rectángulo de la cara

BUFFER_SIZE = 5  # número de frames para suavizar boca
frame_counter = 0
generar_cada = 50  # cada cuántos frames generar fruta
dificultad = 1

# Lista de frutas
frutas = []

def procesar_cara(frame, face_cascade):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)

    if len(faces) > 0:
        x, y, w, h = faces[0]
        dibujar_face(frame, x, y, w, h)
        boca_x = x + w // 2
        boca_y = y + int(h*0.75)  # centro aproximado de la boca
        cv2.circle(frame, (boca_x, boca_y), 5, (0, 255, 255), -1)
        face_roi_gray = gray[y + int(h*0.55):y + h, x:x + w]
        return frame, face_roi_gray, boca_x, boca_y
    else:
        cv2.putText(frame, "Cara no detectada", (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
        return frame, None, None, None

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

def procesar_frame(frame, face_cascade, mouth_cascade, mouth_states, score):
    global frame_counter, frutas
    frame = cv2.flip(frame, 1)
    frame, face_roi_gray, boca_x, boca_y = procesar_cara(frame, face_cascade)

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

    # Eliminar frutas atrapadas por la boca o fuera de pantalla
    nuevas_frutas = []
    for fruta in frutas:
        if boca_x is not None and boca_y is not None and fruta_atrapada_por_boca(fruta, boca_x, boca_y, 50, boca_abierta):
            score[0] += fruta.puntaje
        elif fruta.fuera_de_pantalla(frame.shape[0]):
            continue
        else:
            nuevas_frutas.append(fruta)
    frutas = nuevas_frutas

    # Mostrar puntaje
    cv2.putText(frame, f"Puntaje: {score[0]}", (20, 120), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

    return frame

def main():
    face_cascade, mouth_cascade = cargar_cascades()
    cap = inicializar_camara()
    mouth_states = []
    score = [0]

    print("Presiona 'q' para salir.")
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        frame = procesar_frame(frame, face_cascade, mouth_cascade, mouth_states, score)
        cv2.imshow("CrazyBasket - Fase 2", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
