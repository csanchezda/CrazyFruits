import cv2
from detectors import cargar_cascades
from camera_utils import inicializar_camara
from game import CrazyBasketGame

# Variables globales para el menú
menu_opciones = ["JUGAR", "SALIR"]
menu_rects = []
seleccion = None
estado = "MENU"  # MENU o JUEGO

def dibujar_menu(frame):
    global menu_rects
    frame[:] = (50, 50, 50)  # fondo gris
    h, w = frame.shape[:2]
    menu_rects = []

    for i, texto in enumerate(menu_opciones):
        x1, y1 = int(w*0.35), int(h*(0.4 + i*0.2))
        x2, y2 = int(w*0.65), int(h*(0.5 + i*0.2))
        cv2.rectangle(frame, (x1, y1), (x2, y2), (100, 100, 255), -1)
        cv2.putText(frame, texto, (x1 + 20, y1 + 40),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
        menu_rects.append((x1, y1, x2, y2))
    return frame

def click_event(event, x, y, flags, param):
    global seleccion, estado
    if event == cv2.EVENT_LBUTTONDOWN and estado == "MENU":
        for i, (x1, y1, x2, y2) in enumerate(menu_rects):
            if x1 <= x <= x2 and y1 <= y <= y2:
                seleccion = menu_opciones[i]
                if seleccion == "JUGAR":
                    estado = "JUEGO"
                elif seleccion == "SALIR":
                    estado = "SALIR"

def main():
    global seleccion, estado
    seleccion = None

    # Cargar cascades y cámara
    face_cascade, mouth_cascade = cargar_cascades()
    cap = inicializar_camara()

    # Leer frame para obtener tamaño
    ret, frame = cap.read()
    if not ret:
        print("Error al iniciar la cámara")
        return
    h, w = frame.shape[:2]
    menu_frame = frame.copy()

    cv2.namedWindow("CrazyBasket")
    cv2.setMouseCallback("CrazyBasket", click_event)

    # Crear instancia del juego
    game = CrazyBasketGame(face_cascade, mouth_cascade, w, h)

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        if estado == "MENU":
            dibujar_menu(menu_frame)
            cv2.imshow("CrazyBasket", menu_frame)

        elif estado == "JUEGO":
            frame = game.procesar_frame(frame)
            cv2.imshow("CrazyBasket", frame)

        elif estado == "SALIR":
            break

        key = cv2.waitKey(20) & 0xFF
        if key == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
