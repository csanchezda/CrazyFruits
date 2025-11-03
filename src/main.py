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
campo_nombre_rect = (0, 0, 0, 0)
campo_activo = False
nombre_jugador = ""

# -------------------------------
# Variables de sonido
# -------------------------------
vol_rect = (0, 0, 0, 0)
sonidos = None
game = None

# -------------------------------
# Callback del mouse
# -------------------------------
def click_event(event, x, y, flags, param):
    global estado, sonidos, vol_rect, game, campo_activo, nombre_jugador
    if event == cv2.EVENT_LBUTTONDOWN:
        # --- Icono de sonido ---
        x1, y1, x2, y2 = vol_rect
        if x1 <= x <= x2 and y1 <= y <= y2:
            if sonidos:
                sonidos.toggle_mute()
            return

        # --- Campo de texto nombre ---
        if estado == "MENU":
            x1, y1, x2, y2 = campo_nombre_rect
            if x1 <= x <= x2 and y1 <= y <= y2:
                campo_activo = True
                return
            else:
                campo_activo = False

            # --- Botones menú ---
            for i, (bx1, by1, bx2, by2) in enumerate(menu_rects):
                if bx1 <= x <= bx2 and by1 <= y <= by2:
                    seleccion = menu_opciones[i]
                    if seleccion == "JUGAR":
                        game = CrazyFruitsGame(face_cascade, mouth_cascade, w, h, nombre_jugador=nombre_jugador)
                        sonidos = game.sonidos
                        estado = "JUEGO"
                    elif seleccion == "SALIR":
                        estado = "SALIR"

        elif estado == "GAME_OVER":
            if game and hasattr(game, "boton_reiniciar"):
                x1, y1, x2, y2 = game.boton_reiniciar
                if x1 <= x <= x2 and y1 <= y <= y2:
                    game = CrazyFruitsGame(face_cascade, mouth_cascade, w, h, nombre_jugador=nombre_jugador)
                    sonidos = game.sonidos
                    estado = "JUEGO"

# -------------------------------
# Función principal
# -------------------------------
def main():
    global estado, sonidos, vol_rect, campo_nombre_rect, game, face_cascade, mouth_cascade, w, h, nombre_jugador

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

    while True:
        ret, frame = cap.read()
        frame = cv2.flip(frame, 1)

        if not ret:
            break

        if estado == "MENU":
            campo_nombre_rect = graphics.dibujar_menu(frame, menu_opciones, menu_rects, nombre_jugador)

        elif estado == "JUEGO":
            frame = game.procesar_frame(frame)
            if game.game_over:
                estado = "GAME_OVER"

        elif estado == "GAME_OVER":
            game.mostrar_game_over(frame)

        elif estado == "SALIR":
            break

        # --- Icono de sonido ---
        if sonidos:
            vol_rect = graphics.dibujar_icono_sonido(frame, sonidos.muted, x=w - 70, y=20, tam=40)

        cv2.imshow("CrazyFruits", frame)
        key = cv2.waitKey(20) & 0xFF

        # --- Salir ---
        if key in (ord('q'), ord('Q')):
            break

        # --- Escribir nombre ---
        if campo_activo and estado == "MENU":
            if 32 <= key <= 126:
                nombre_jugador += chr(key)
            elif key in (8, 127):
                nombre_jugador = nombre_jugador[:-1]

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
