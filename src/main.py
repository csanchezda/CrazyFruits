import cv2
import os
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
# Variables globales
# -------------------------------
vol_rect = (0, 0, 0, 0)
sonidos = None

# -------------------------------
# Callback del mouse
# -------------------------------
def click_event(event, x, y, flags, param):
    global estado, sonidos, vol_rect
    if event == cv2.EVENT_LBUTTONDOWN:
        # --- Icono de sonido ---
        x1, y1, x2, y2 = vol_rect
        if x1 <= x <= x2 and y1 <= y <= y2:
            if sonidos:
                sonidos.toggle_mute()
            return

        # --- Menú principal ---
        if estado == "MENU":
            for i, (x1, y1, x2, y2) in enumerate(menu_rects):
                if x1 <= x <= x2 and y1 <= y <= y2:
                    seleccion = menu_opciones[i]
                    if seleccion == "JUGAR":
                        estado = "JUEGO"
                    elif seleccion == "SALIR":
                        estado = "SALIR"

        # --- Click en GAME OVER vuelve al menú ---
        elif estado == "GAME_OVER":
            estado = "MENU"
            sonidos.reanudar_musica()

# -------------------------------
# Función principal
# -------------------------------
def main():
    global estado, sonidos, vol_rect

    # Cargar cascades y cámara
    face_cascade, mouth_cascade = cargar_cascades()
    cap = inicializar_camara()

    ret, frame = cap.read()
    if not ret:
        print("Error al iniciar la cámara")
        return

    h, w = frame.shape[:2]
    cv2.namedWindow("CrazyFruits")
    cv2.setMouseCallback("CrazyFruits", click_event)

    # Instanciar juego y sonidos
    game = CrazyFruitsGame(face_cascade, mouth_cascade, w, h)
    sonidos = game.sonidos

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # -------------------------------
        # Estados
        # -------------------------------
        if estado == "MENU":
            graphics.dibujar_menu(frame, menu_opciones, menu_rects)

        elif estado == "JUEGO":
            frame = game.procesar_frame(frame)
            if game.game_over:
                sonidos.play_game_over()
                estado = "GAME_OVER"

        elif estado == "GAME_OVER":
            game.mostrar_game_over(frame)

        elif estado == "SALIR":
            break

        # -------------------------------
        # Icono de sonido
        # -------------------------------
        vol_rect = graphics.dibujar_icono_sonido(frame, sonidos.muted, x=w-70, y=20, tam=40)

        cv2.imshow("CrazyFruits", frame)

        key = cv2.waitKey(20) & 0xFF
        if key == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
