import cv2
from camera_utils import inicializar_camara
from detectors import cargar_cascades, detectar_boca
from draw_utils import dibujar_cesta, dibujar_face

BUFFER_SIZE = 5  # número de frames para promediar

def procesar_cara_y_cesta(frame, face_cascade, smooth_x, alpha, basket_width=120, basket_y_offset=60):
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
        return frame, smooth_x, face_roi_gray
    else:
        cv2.putText(frame, "Cara no detectada", (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
        return frame, smooth_x, None

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

def procesar_frame(frame, face_cascade, mouth_cascade, smooth_x, alpha, mouth_states):
    frame = cv2.flip(frame, 1)
    frame, smooth_x, face_roi_gray = procesar_cara_y_cesta(frame, face_cascade, smooth_x, alpha)
    
    if face_roi_gray is not None:
        is_open = detectar_boca(face_roi_gray, mouth_cascade)
        is_open_smooth = boca_abierta_promediada(is_open, mouth_states)
        frame = procesar_boca_y_texto(frame, is_open_smooth)
    
    return frame, smooth_x

def main():
    face_cascade, mouth_cascade = cargar_cascades()
    cap = inicializar_camara()
    smooth_x = None
    alpha = 0.2
    mouth_states = []

    print("Presiona 'q' para salir.")
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        frame, smooth_x = procesar_frame(frame, face_cascade, mouth_cascade, smooth_x, alpha, mouth_states)
        cv2.imshow("CrazyBasket - Fase 0", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
