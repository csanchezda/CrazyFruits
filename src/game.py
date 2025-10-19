# game.py
import cv2
from fruta import Fruta, generar_fruta, atrapada_por_boca
from particulas import Particula
from detectors import detectar_boca
from vida import Vida
import graphics

BUFFER_SIZE = 5

class CrazyFruitsGame:
    def __init__(self, face_cascade, mouth_cascade, frame_width, frame_height, vidas=3):
        self.face_cascade = face_cascade
        self.mouth_cascade = mouth_cascade
        self.frame_width = frame_width
        self.frame_height = frame_height

        self.frutas = []
        self.particulas = []
        self.mouth_states = []
        self.score = 0
        self.vidas = Vida(vidas)
        self.frame_counter = 0
        self.generar_cada = 50
        self.dificultad = 1
        self.game_over = False

    # -------------------------------
    # Lógica de boca
    # -------------------------------
    def boca_abierta_promediada(self, is_open):
        self.mouth_states.append(is_open)
        if len(self.mouth_states) > BUFFER_SIZE:
            self.mouth_states.pop(0)
        return sum(self.mouth_states) > BUFFER_SIZE // 2

    # -------------------------------
    # Procesamiento de cara y boca
    # -------------------------------
    def procesar_cara(self, frame):
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = self.face_cascade.detectMultiScale(gray, 1.3, 5)

        if len(faces) > 0:
            x, y, w, h = faces[0]
            face_center_x = graphics.dibujar_face(frame, x, y, w, h)
            boca_x = x + w // 2
            boca_y = y + int(h*0.75)
            graphics.dibujar_boca(frame, boca_x, boca_y)
            face_roi_gray = gray[y + int(h*0.55):y + h, x:x + w]
            return frame, face_roi_gray, boca_x, boca_y
        else:
            cv2.putText(frame, "Cara no detectada", (20, 40),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
            return frame, None, None, None

    # -------------------------------
    # Procesamiento de un frame completo
    # -------------------------------
    def procesar_frame(self, frame):
        frame = cv2.flip(frame, 1)

        if self.game_over:
            self.mostrar_game_over(frame)
            return frame

        frame, face_roi_gray, boca_x, boca_y = self.procesar_cara(frame)

        # Boca abierta
        if face_roi_gray is not None:
            is_open = detectar_boca(face_roi_gray, self.mouth_cascade)
            boca_abierta = self.boca_abierta_promediada(is_open)
        else:
            boca_abierta = False

        # Generar frutas
        self.frame_counter += 1
        if self.frame_counter % self.generar_cada == 0:
            self.frutas.append(generar_fruta(frame.shape[1], self.dificultad))

        # Mover y dibujar frutas
        for fruta in self.frutas:
            fruta.mover()
            graphics.dibujar_fruta(frame, fruta)

        # Verificar frutas atrapadas y fuera de pantalla
        nuevas_frutas = []
        for fruta in self.frutas:
            if boca_x is not None and boca_y is not None and atrapada_por_boca(fruta, boca_x, boca_y, 50, boca_abierta):
                self.score += fruta.puntaje
                self.particulas.extend([
                    Particula(fruta.x, fruta.y, graphics.FRUTA_COLORES.get(fruta.tipo, (255, 255, 255)))
                    for _ in range(15)
                ])
            elif fruta.fuera_de_pantalla(frame.shape[0]):
                self.vidas.perder_vida()
                if self.vidas.actual <= 0:
                    self.game_over = True
            else:
                nuevas_frutas.append(fruta)
        self.frutas = nuevas_frutas

        # Mover y dibujar partículas
        nuevas_particulas = []
        for p in self.particulas:
            p.mover()
            if p.vida > 0:
                graphics.dibujar_particula(frame, p)
                nuevas_particulas.append(p)
        self.particulas = nuevas_particulas

        # Dibujar puntaje y vidas usando graphics.py
        graphics.dibujar_puntaje(frame, self.score, x=20, y=80)
        graphics.dibujar_vidas(frame, self.vidas.actual, self.vidas.total, x=20, y=120)

        return frame

    # -------------------------------
    # Pantalla de Game Over
    # -------------------------------
    def mostrar_game_over(self, frame):
        frame[:] = (0, 0, 0)
        h, w = frame.shape[:2]
        cv2.putText(frame, "GAME OVER", (w//4, h//2 - 50),
                    cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 255), 4)
        cv2.putText(frame, f"Puntaje final: {self.score}", (w//4, h//2 + 50),
                    cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 255, 0), 3)
        cv2.putText(frame, "Presiona 'q' para salir", (w//4, h//2 + 120),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
