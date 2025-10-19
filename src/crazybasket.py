import os
import cv2

# Carpeta del script
script_dir = os.path.dirname(os.path.abspath(__file__))
cascade_path = os.path.join(script_dir, "haarcascade_mcs_mouth.xml")

# Cargar el cascade de boca
mouth_cascade = cv2.CascadeClassifier(cascade_path)
if mouth_cascade.empty():
    print("ERROR: No se pudo cargar el cascade de boca!")
    exit()

# Inicializa la cámara
cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("ERROR: No se pudo abrir la cámara!")
    exit()

# Clasificador de cara
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")

# Variables de la cesta
basket_width = 120
basket_height = 25
basket_y_offset = 60
smooth_x = None
alpha = 0.2

print("Presiona 'q' para salir.")

while True:
    ret, frame = cap.read()
    if not ret:
        print("No se pudo leer el frame.")
        break

    frame = cv2.flip(frame, 1)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    frame_height, frame_width = frame.shape[:2]

    faces = face_cascade.detectMultiScale(gray, 1.3, 5)
    
    if len(faces) > 0:
        x, y, w, h = faces[0]
        face_center_x = x + w // 2

        # Dibuja la cara
        cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 150, 0), 2)
        cv2.line(frame, (face_center_x, 0), (face_center_x, frame_height), (0, 255, 255), 1)

        # Posición de la cesta con suavización
        target_x = int(face_center_x / frame_width * (frame_width - basket_width))
        if smooth_x is None:
            smooth_x = target_x
        else:
            smooth_x = int(smooth_x * (1 - alpha) + target_x * alpha)
        basket_y = frame_height - basket_y_offset
        cv2.rectangle(frame, (smooth_x, basket_y), (smooth_x + basket_width, basket_y + basket_height), (0, 255, 0), -1)

        # --- Detección de boca ---
        face_roi_gray = gray[y + int(h*0.5):y + h, x:x + w]
        mouths = mouth_cascade.detectMultiScale(face_roi_gray, 1.5, 11)
        mouth_open = True  # asumimos abierta
        for (mx, my, mw, mh) in mouths:
            # si detecta una boca (el cascade encuentra boca cerrada), entonces NO está abierta
            mouth_open = False
            break


        if mouth_open:
            cv2.putText(frame, "Boca abierta!", (20, 80), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)
        else:
            cv2.putText(frame, "Boca cerrada", (20, 80), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (200, 200, 200), 2)

    else:
        cv2.putText(frame, "Cara no detectada", (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

    # Mostrar frame
    cv2.imshow("CrazyBasket - Fase 0", frame)

    # Detectar tecla 'q' para salir
    key = cv2.waitKey(1)
    if key != -1:
        print(f"Tecla presionada: {key}")  # debug
    if key & 0xFF == ord('q'):
        print("Saliendo...")
        break

cap.release()
cv2.destroyAllWindows()
