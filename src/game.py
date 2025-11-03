import cv2
from fruta import Fruta, generar_fruta, atrapada_por_boca
from particulas import Particula
from detectors import detectar_boca
from vida import Vida
from sound_manager import SoundManager
from score_manager import guardar_puntaje, obtener_mejores
import graphics

BUFFER_SIZE = 5

class CrazyFruitsGame:
    def __init__(self, face_cascade, mouth_cascade, frame_width, frame_height, nombre_jugador="Player"):
        self.face_cascade = face_cascade
        self.mouth_cascade = mouth_cascade
        self.frame_width = frame_width
        self.frame_height = frame_height
        self.nombre_jugador = nombre_jugador.strip() or "Player"

        self.frutas = []
        self.particulas = []
        self.mouth_states = []
        self.score = 0
        self.vidas = Vida(3)
        self.frame_counter = 0
        self.generar_cada = 50
        self.dificultad = 1
        self.game_over = False

        # Sonidos
        self.sonidos = SoundManager()

    def boca_abierta_promediada(self, is_open):
        self.mouth_states.append(is_open)
        if len(self.mouth_states) > BUFFER_SIZE:
            self.mouth_states.pop(0)
        return sum(self.mouth_states) > BUFFER_SIZE // 2

    def procesar_cara(self, frame):
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
            sombra = (30, 30, 30)
            color = (255, 220, 100)
            cv2.putText(frame, "Cara no detectada", (22, 42),
                        cv2.FONT_HERSHEY_DUPLEX, 0.8, sombra, 2, cv2.LINE_AA)
            cv2.putText(frame, "Cara no detectada", (20, 40),
                        cv2.FONT_HERSHEY_DUPLEX, 0.8, color, 1, cv2.LINE_AA)
            return frame, None, None, None

    def procesar_frame(self, frame):

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
        for fruta in self.frutas:
            fruta.mover()
            graphics.dibujar_fruta(frame, fruta)

            if boca_x and boca_y and atrapada_por_boca(fruta, boca_x, boca_y, 50, boca_abierta):
                self.score += fruta.puntaje
                self.sonidos.play_comer()
                self.particulas.extend([
                    Particula(fruta.x, fruta.y, graphics.FRUTA_COLORES.get(fruta.tipo, (255, 255, 255)))
                    for _ in range(15)
                ])
            elif fruta.fuera_de_pantalla(frame.shape[0]):
                self.vidas.perder_vida()
                self.sonidos.play_perder()
                if self.vidas.actual <= 0:
                    guardar_puntaje(self.score, self.nombre_jugador)
                    self.sonidos.play_game_over()
                    self.game_over = True
            else:
                nuevas_frutas.append(fruta)
        self.frutas = nuevas_frutas

        nuevas_particulas = []
        for p in self.particulas:
            p.mover()
            if p.vida > 0:
                graphics.dibujar_particula(frame, p)
                nuevas_particulas.append(p)
        self.particulas = nuevas_particulas

        graphics.dibujar_puntaje(frame, self.score, x=20, y=80)
        graphics.dibujar_vidas(frame, self.vidas.actual, x=20, y=120, animaciones=self.vidas.animaciones)

        return frame

    def mostrar_game_over(self, frame):
        frame[:] = (0, 0, 0)
        h, w = frame.shape[:2]
        font = cv2.FONT_HERSHEY_DUPLEX

        title = "GAME OVER"
        (tw, th), _ = cv2.getTextSize(title, font, 2, 4)
        cv2.putText(frame, title, ((w - tw) // 2, h // 2 - 200), font, 2, (0, 0, 255), 4)

        jugador = f"Jugador: {self.nombre_jugador}"
        cv2.putText(frame, jugador, (w//2 - 200, h//2 - 130), font, 1, (255, 255, 255), 2)

        final_score = f"Puntaje: {self.score}"
        cv2.putText(frame, final_score, (w//2 - 160, h//2 - 80), font, 1.3, (0, 255, 0), 3)

        top = obtener_mejores(5)
        cv2.putText(frame, "TOP 5:", (w//2 - 80, h//2 - 20), font, 1, (255, 255, 0), 2)
        for i, t in enumerate(top):
            cv2.putText(frame, f"{i+1}. {t['nombre']} - {t['score']}", (w//2 - 150, h//2 + 40 + i * 35),
                        font, 0.8, (200, 200, 200), 2)

        btn_w, btn_h = 300, 70
        btn_x1 = (w - btn_w)//2
        btn_y1 = h - 150
        btn_x2 = btn_x1 + btn_w
        btn_y2 = btn_y1 + btn_h

        cv2.rectangle(frame, (btn_x1, btn_y1), (btn_x2, btn_y2), (0, 255, 0), -1)
        btn_text = "VOLVER A JUGAR"
        (bw, bh), _ = cv2.getTextSize(btn_text, font, 1, 3)
        bx = btn_x1 + (btn_w - bw)//2
        by = btn_y1 + (btn_h + bh)//2 - 5
        cv2.putText(frame, btn_text, (bx, by), font, 1, (0, 0, 0), 3)

        self.boton_reiniciar = (btn_x1, btn_y1, btn_x2, btn_y2)
