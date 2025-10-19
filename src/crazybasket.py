import os
import cv2

def cargar_cascades():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    mouth_cascade = cv2.CascadeClassifier(os.path.join(script_dir, "haarcascade_mcs_mouth.xml"))
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
    if mouth_cascade.empty() or face_cascade.empty():
        raise RuntimeError("No se pudieron cargar los cascades")
    return face_cascade, mouth_cascade

def inicializar_camara():
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        raise RuntimeError("No se pudo abrir la cámara")
    return cap

def detectar_boca(face_roi_gray, mouth_cascade):
    mouths = mouth_cascade.detectMultiScale(face_roi_gray, 1.5, 11)
    return len(mouths) == 0  # True si boca abierta

def dibujar_cesta(frame, basket_x, basket_y, basket_width=120, basket_height=25):
    cv2.rectangle(frame, (basket_x, basket_y), (basket_x + basket_width, basket_y + basket_height), (0, 255, 0), -1)

def procesar_frame(frame, face_cascade, mouth_cascade, smooth_x, alpha):
    frame = cv2.flip(frame, 1)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    frame_height, frame_width = frame.shape[:2]

    faces = face_cascade.detectMultiScale(gray, 1.3, 5)
    
    if len(faces) > 0:
        x, y, w, h = faces[0]
        face_center_x = x + w // 2

        cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 150, 0), 2)
        cv2.line(frame, (face_center_x, 0), (face_center_x, frame_height), (0, 255, 255), 1)

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
