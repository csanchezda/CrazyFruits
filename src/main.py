# main.py

import cv2
from detectors import cargar_cascades
from camera_utils import inicializar_camara
from game import CrazyFruitsGame
import graphics

# -------------------------------
# Configuración del menú
# -------------------------------
menu_opciones = ["JUGAR", "SALIR"]
menu_rects = []
estado = "MENU"  # MENU, JUEGO, GAME_OVER, SALIR

# -------------------------------
# Callback del mouse
# -------------------------------
def click_event(event, x, y, flags, param):
    global estado
    if event == cv2.EVENT_LBUTTONDOWN:
        if estado == "MENU":
            for i, (x1, y1, x2, y2) in enumerate(menu_rects):
                if x1 <= x <= x2 and y1 <= y <= y2:
                    seleccion = menu_opciones[i]
                    if seleccion == "JUGAR":
                        estado = "JUEGO"
                    elif seleccion == "SALIR":
                        estado = "SALIR"
        elif estado == "GAME_OVER":
            # cualquier click vuelve al menú
            estado = "MENU"

# -------------------------------
# Función principal
# -------------------------------
def main():
    global estado

    # Cargar cascades y cámara
    face_cascade, mouth_cascade = cargar_cascades()
    cap = inicializar_camara()

    # Leer un frame inicial para obtener dimensiones
    ret, frame = cap.read()
    if not ret:
        print("Error al iniciar la cámara")
        return
    h, w = frame.shape[:2]
    menu_frame = frame.copy()

    # Crear ventana y callback
    cv2.namedWindow("CrazyFruits")
    cv2.setMouseCallback("CrazyFruits", click_event)

    # Instanciar juego
    game = CrazyFruitsGame(face_cascade, mouth_cascade, w, h)

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # -------------------------------
        # Gestión de estados
        # -------------------------------
        if estado == "MENU":
            graphics.dibujar_menu(menu_frame, menu_opciones, menu_rects)
            cv2.imshow("CrazyFruits", menu_frame)

        elif estado == "JUEGO":
            frame = game.procesar_frame(frame)
            cv2.imshow("CrazyFruits", frame)
            if game.game_over:
                estado = "GAME_OVER"

        elif estado == "GAME_OVER":
            game.mostrar_game_over(frame)
            cv2.imshow("CrazyFruits", frame)

        elif estado == "SALIR":
            break

        # -------------------------------
        # Tecla para salir
        # -------------------------------
        key = cv2.waitKey(20) & 0xFF
        if key == ord('q'):
            break

    # -------------------------------
    # Liberar recursos
    # -------------------------------
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
