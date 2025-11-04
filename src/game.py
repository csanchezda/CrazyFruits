"""
Lógica principal del juego: manejo de frutas, detección de boca y estados.

Contiene la clase `CrazyFruitsGame` que encapsula el estado del juego,
la física simple de las frutas, efectos visuales (partículas) y la
gestión de vidas y puntaje.
"""

import cv2
from fruta import TipoFruta, Fruta, generar_fruta, atrapada_por_boca
from particulas import Particula
from detectors import detectar_boca
from vida import Vida
from score_manager import guardar_puntaje, obtener_mejores
import graphics
import threading
import time
import os

BUFFER_SIZE = 5

class CrazyFruitsGame:
    """Clase que representa una sesión de juego.

    Atributos clave:
    - frutas: lista de objetos `Fruta` activos
    - particulas: partículas para efectos visuales al comer
    - vidas: instancia de `Vida` que controla la vida del jugador
    - score: puntaje acumulado
    """
    def __init__(self, face_cascade, mouth_cascade, frame_width, frame_height, nombre_jugador="Player", sonidos=None):
        self.face_cascade = face_cascade
        self.mouth_cascade = mouth_cascade
        self.frame_width = frame_width
        self.frame_height = frame_height
        self.nombre_jugador = nombre_jugador.strip() or "Player"

        self.frutas = []
        self.particulas = []
        self.mouth_states = []
        self.score = 0
        self.vidas = Vida(4)
        self.frame_counter = 0
        self.generar_cada = 30 # Frutas cada n frames
        self.dificultad = 1 
        self.last_dificultad_time = time.time()
        self.game_over = False
        self.sonidos = sonidos

    def boca_abierta_promediada(self, is_open):
        """Mantiene un buffer de últimos estados de la boca y devuelve
        si en promedio la boca está abierta (reducción de ruido en detección).
        """
        self.mouth_states.append(is_open)
        if len(self.mouth_states) > BUFFER_SIZE:
            self.mouth_states.pop(0)
        return sum(self.mouth_states) > BUFFER_SIZE // 2

    def procesar_cara(self, frame):
        """Detecta la cara y retorna la región de interés (ROI) en escala de grises
        que se usará para detectar si la boca está abierta. Además dibuja
        indicaciones en el frame (rectángulo de cara y punto de boca).
        """
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = self.face_cascade.detectMultiScale(gray, 1.3, 5)
        if len(faces) > 0:
            x, y, w, h = faces[0]
            face_center_x = graphics.dibujar_face(frame, x, y, w, h)
            boca_x = x + w // 2
            boca_y = y + int(h * 0.75)
            graphics.dibujar_boca(frame, boca_x, boca_y)
            face_roi_gray = gray[y + int(h * 0.55):y + h, x:x + w]
            return frame, face_roi_gray, boca_x, boca_y
        else:
            # Si no detecta cara, muestra un aviso y devuelve None en ROI
            sombra = (30, 30, 30)
            color = (255, 220, 100)
            cv2.putText(frame, "Cara no detectada", (22, 42),
                        cv2.FONT_HERSHEY_DUPLEX, 0.8, sombra, 2, cv2.LINE_AA)
            cv2.putText(frame, "Cara no detectada", (20, 40),
                        cv2.FONT_HERSHEY_DUPLEX, 0.8, color, 1, cv2.LINE_AA)
            return frame, None, None, None

    def aumentar_dificultad(self):
        """
        Aumenta progresivamente la dificultad del juego:
        - Incrementa la velocidad de caída de las frutas (multiplicador)
        - Disminuye el tiempo entre la generación de frutas
        """
        now = time.time()
        # Cada 10 segundos reales: aumentar la dificultad y reducir la frecuencia de generación
        if now - self.last_dificultad_time > 10:
            self.dificultad += 0.3
            if self.generar_cada > 10:
                self.generar_cada -= 2
            self.last_dificultad_time = now
            print("[DIFICULTAD]:", self.dificultad, "Generar cada:", self.generar_cada)
        return

    def procesar_frame(self, frame):
        """Procesa un frame: detección de cara/boca, movimiento y colisiones de frutas,
        actualiza partículas, dibuja HUD y devuelve el frame modificado listo para mostrar.
        """
        self.aumentar_dificultad()
        if self.game_over:
            self.mostrar_game_over(frame)
            return frame

        frame, face_roi_gray, boca_x, boca_y = self.procesar_cara(frame)

        if face_roi_gray is not None:
            is_open = detectar_boca(face_roi_gray, self.mouth_cascade)
            boca_abierta = self.boca_abierta_promediada(is_open)
        else:
            boca_abierta = False

        self.frame_counter += 1
        if self.frame_counter % self.generar_cada == 0:
            self.frutas.append(generar_fruta(frame.shape[1], self.dificultad))

        nuevas_frutas = []

        # --- Recorremos todas las frutas ---
        for fruta in self.frutas:
            fruta.mover()

            atrapada = (
                boca_x and boca_y and
                atrapada_por_boca(fruta, boca_x, boca_y, 50, boca_abierta)
            )

            if atrapada:
                if fruta.tipo == TipoFruta.MIX:
                    self.vidas.ganar_vida()
                    threading.Thread(target=self.sonidos.play_ganar, daemon=True).start()
                elif fruta.tipo == TipoFruta.BOMB:
                    self.vidas.perder_vida()
                    threading.Thread(target=self.sonidos.play_perder, daemon=True).start()
                else:
                    self.score += fruta.puntaje
                    threading.Thread(target=self.sonidos.play_comer, daemon=True).start()

                # --- Efecto visual ---
                self.particulas.extend([
                    Particula(
                        fruta.x, fruta.y,
                        graphics.FRUTA_COLORES_BGR.get(fruta.tipo.name, (255, 255, 255))  # default blanco
                    )
                    for _ in range(15)
                ])
                continue

            elif fruta.fuera_de_pantalla(frame.shape[0]):
                if fruta.tipo != TipoFruta.MIX and fruta.tipo != TipoFruta.BOMB:
                    self.vidas.perder_vida()
                    threading.Thread(target=self.sonidos.play_perder, daemon=True).start()
                    if self.vidas.actual <= 0:
                        guardar_puntaje(self.score, self.nombre_jugador)
                        threading.Thread(target=self.sonidos.play_game_over, daemon=True).start()
                        self.game_over = True
                continue

            # --- Solo dibujar frutas activas ---
            graphics.dibujar_fruta(frame, fruta)
            nuevas_frutas.append(fruta)

        self.frutas = nuevas_frutas

        # --- Actualizar partículas ---
        nuevas_particulas = []
        for p in self.particulas:
            p.mover()
            if p.vida > 0:
                graphics.dibujar_particula(frame, p)
                nuevas_particulas.append(p)
        self.particulas = nuevas_particulas

        # --- Dibujar HUD ---
        graphics.dibujar_puntaje(frame, self.score, x=20, y=80)
        graphics.dibujar_vidas(frame, self.vidas.actual, x=20, y=120, animaciones=self.vidas.animaciones, animaciones_ganar=self.vidas.animaciones_ganar)
        # Dibujar dificultad
        dificultad_texto = f"Dificultad: {self.dificultad:.1f}"
        cv2.putText(frame, dificultad_texto, (20, 200),
            cv2.FONT_HERSHEY_DUPLEX, 0.6, (255, 200, 0), 1, cv2.LINE_AA)


        return frame

    def mostrar_game_over(self, frame):
        gameover_path = os.path.join("assets", "icons", "gameOverBackground.png")
        gameOverBackground = cv2.imread(gameover_path)
        if gameOverBackground is None:
            print("No se pudo cargar gameOverBackground, usando fondo negro.")
        """
        Muestra la pantalla de Game Over con fondo de frutas si se proporciona.

        Dibuja además el TOP 5 de puntajes y un botón para reiniciar la partida.
        """
        h, w = frame.shape[:2]

        # --- Fondo ---
        if gameOverBackground is not None:
            # Redimensionar al tamaño del frame
            fondo_resized = cv2.resize(gameOverBackground, (w, h))
            frame[:] = fondo_resized
        else:
            frame[:] = (0, 0, 0)  # fallback negro

        font = cv2.FONT_HERSHEY_DUPLEX

        # --- Título ---
        title = "GAME OVER"
        (tw, th), _ = cv2.getTextSize(title, font, 2, 4)
        cx, cy = (w - tw)//2, h//2 - 220
        cv2.putText(frame, title, (cx+4, cy+4), font, 2, (50, 50, 50), 6, cv2.LINE_AA)  # sombra
        cv2.putText(frame, title, (cx, cy), font, 2, (0, 0, 255), 4, cv2.LINE_AA)

        # --- Nombre del jugador ---
        jugador_text = f"Jugador: {self.nombre_jugador}"
        (jw, jh), _ = cv2.getTextSize(jugador_text, font, 1, 2)
        cv2.putText(frame, jugador_text, ((w - jw)//2, h//2 - 150), font, 1, (50, 30, 100), 2)  # violeta oscuro

        # --- Puntaje final ---
        final_score = f"Puntaje: {self.score}"
        (sw, sh), _ = cv2.getTextSize(final_score, font, 1.5, 3)
        cv2.putText(frame, final_score, ((w - sw)//2, h//2 - 90), font, 1.5, (39, 245, 42), 3)  # verde

        # --- TOP 5 ---
        top = obtener_mejores(5)
        top_title = "TOP 5"
        (top_tw, _), _ = cv2.getTextSize(top_title, font, 1, 2)
        cv2.putText(frame, top_title, ((w - top_tw)//2, h//2 - 20), font, 1, (0, 60, 150), 2)  # azul oscuro

        # Ajustar listado de jugadores centrado
        for i, t in enumerate(top):
            text = f"{i+1}. {t['nombre']} - {t['score']}"
            (text_w, text_h), _ = cv2.getTextSize(text, font, 0.8, 2)
            x = (w - text_w)//2
            y = h//2 + 40 + i*30
            cv2.putText(frame, text, (x, y-15), font, 0.8, (80, 80, 80), 2)  # gris oscuro para buen contraste

        # --- Botón volver a jugar ---
        btn_w, btn_h = 300, 70

        btn_y1 = h - 180
        btn_y2 = btn_y1 + btn_h
        btn_x1 = (w - btn_w)//2
        btn_x2 = btn_x1 + btn_w

        # Dibujar rectángulo y borde
        cv2.rectangle(frame, (btn_x1, btn_y1), (btn_x2, btn_y2), (0, 200, 0), -1)
        cv2.rectangle(frame, (btn_x1, btn_y1), (btn_x2, btn_y2), (0, 100, 0), 3)  # borde

        # Texto centrado en el botón
        btn_text = "VOLVER A JUGAR"
        (bw, bh), _ = cv2.getTextSize(btn_text, font, 1, 3)
        bx = btn_x1 + (btn_w - bw)//2
        by = btn_y1 + (btn_h + bh)//2 - 5
        cv2.putText(frame, btn_text, (bx, by), font, 1, (0, 0, 0), 3)

        self.boton_reiniciar = (btn_x1, btn_y1, btn_x2, btn_y2)