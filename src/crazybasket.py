import cv2
from camera_utils import inicializar_camara
from detectors import cargar_cascades, detectar_boca
from draw_utils import dibujar_cesta, dibujar_face

def procesar_frame(frame, face_cascade, mouth_cascade, smooth_x, alpha):
    frame = cv2.flip(frame, 1)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    frame_height, frame_width = frame.shape[:2]

    faces = face_cascade.detectMultiScale(gray, 1.3, 5)
    
    if len(faces) > 0:
        x, y, w, h = faces[0]
        face_center_x = dibujar_face(frame, x, y, w, h)

        target_x = int(face_center_x / frame_width * (frame_width - 120))
        smooth_x = target_x if smooth_x is None else int(smooth_x * (1 - alpha) + target_x * alpha)
        basket_y = frame_height - 60
        dibujar_cesta(frame, smooth_x, basket_y)

        face_roi_gray = gray[y + int(h*0.5):y + h, x:x + w]
        if detectar_boca(face_roi_gray, mouth_cascade):
            cv2.putText(frame, "Boca abierta!", (20, 80), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)
        else:
            cv2.putText(frame, "Boca cerrada", (20, 80), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (200, 200, 200), 2)
    else:
        cv2.putText(frame, "Cara no detectada", (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

    return frame, smooth_x

def main():
    face_cascade, mouth_cascade = cargar_cascades()
    cap = inicializar_camara()
    smooth_x = None
    alpha = 0.2

    print("Presiona 'q' para salir.")
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        frame, smooth_x = procesar_frame(frame, face_cascade, mouth_cascade, smooth_x, alpha)
        cv2.imshow("CrazyBasket - Fase 0", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
