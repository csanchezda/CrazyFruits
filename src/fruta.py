import random

class Fruta:
    def __init__(self, x, y, tipo, velocidad):
        self.x = x
        self.y = y
        self.tipo = tipo          # 'manzana', 'banana', 'naranja'
        self.velocidad = velocidad
        self.tam = 40             # tamaño de la fruta
        self.puntaje = self.puntaje_por_tipo(tipo)

    def puntaje_por_tipo(self, tipo):
        puntajes = {
            'manzana': 10,
            'platano': 5,
            'naranja': 8
        }
        return puntajes.get(tipo, 0)

    def mover(self):
        self.y += self.velocidad
    
    def fuera_de_pantalla(self, frame_height):
        return self.y - self.tam // 2 > frame_height

def generar_fruta(frame_width, dificultad=1):
    # Genera una nueva fruta en posición aleatoria arriba de la pantalla.
    x = random.randint(50, frame_width - 50)
    y = -40  # comienza fuera de la pantalla
    tipos = ['manzana', 'platano', 'naranja']
    tipo = random.choice(tipos)
    velocidad = random.randint(3, 5) * dificultad
    return Fruta(x, y, tipo, velocidad)

def atrapada_por_boca(fruta, boca_x, boca_y, boca_radio, boca_abierta):
    """
    Verifica si la fruta está cerca de la boca abierta.
    boca_x, boca_y: centro de la boca (aprox)
    boca_radio: radio de proximidad para atrapar
    """
    if not boca_abierta:
        return False

    distancia = ((fruta.x - boca_x) ** 2 + (fruta.y - boca_y) ** 2) ** 0.5
    return distancia <= boca_radio
