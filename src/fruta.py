import random
import cv2

class Fruta:
    def __init__(self, x, y, tipo, velocidad):
        self.x = x
        self.y = y
        self.tipo = tipo          # 'manzana', 'banana', 'naranja'...
        self.velocidad = velocidad
        self.tam = 40             # tamaño de la fruta
        self.color = self.color_por_tipo(tipo)
        self.puntaje = self.puntaje_por_tipo(tipo)

    def color_por_tipo(self, tipo):
        colores = {
            'manzana': (0, 255, 0),   # verde
            'banana': (255, 255, 0),   # amarillo
            'naranja': (0, 165, 255)   # naranja
        }
        return colores.get(tipo, (255, 255, 255))  # blanco por defecto

    def puntaje_por_tipo(self, tipo):
        puntajes = {
            'manzana': 10,
            'banana': 5,
            'naranja': 8
        }
        return puntajes.get(tipo, 0)

    def mover(self):
        self.y += self.velocidad
    
    def dibujar(self, frame):
        cv2.circle(frame, (self.x, self.y), self.tam // 2, self.color, -1)

    def fuera_de_pantalla(self, frame_height):
        return self.y - self.tam // 2 > frame_height
    
    
def generar_fruta(frame_width, dificultad=1):
    """Genera una nueva fruta en posición aleatoria arriba de la pantalla."""
    x = random.randint(50, frame_width - 50)
    y = -40  # comienza fuera de la pantalla
    tipos = ['manzana', 'banana', 'naranja']
    tipo = random.choice(tipos)
    velocidad = random.randint(3, 5) * dificultad
    return Fruta(x, y, tipo, velocidad)

def fruta_atrapada_por_boca(fruta, boca_x, boca_y, boca_radio, boca_abierta):
    """
    Verifica si la fruta está cerca de la boca abierta.
    boca_x, boca_y: centro de la boca (aprox)
    boca_radio: radio de proximidad para atrapar
    """
    if not boca_abierta:
        return False

    distancia = ((fruta.x - boca_x) ** 2 + (fruta.y - boca_y) ** 2) ** 0.5
    return distancia <= boca_radio
