# fruta.py

import random

class Fruta:
    def __init__(self, x, y, tipo, velocidad, tam, puntaje):
        self.x = x
        self.y = y
        self.tipo = tipo # 'sandia', 'platano', 'manzana'
        self.velocidad = velocidad
        self.tam = tam
        self.puntaje = puntaje

    def mover(self):
        self.y += self.velocidad
    
    def fuera_de_pantalla(self, frame_height):
        return self.y - self.tam // 2 > frame_height


def generar_fruta(frame_width, dificultad=1):
    """
    Genera una nueva fruta con atributos según el tipo.
    La dificultad multiplica la velocidad base.
    """
    x = random.randint(50, frame_width - 50)
    y = -40  # empieza fuera de pantalla
    tipos = ['sandia', 'platano', 'manzana']
    tipo = random.choice(tipos)

    # Configuración por tipo
    if tipo == 'sandia':
        tam = 60
        velocidad = random.uniform(2, 3) * dificultad
        puntaje = 10
    elif tipo == 'platano':
        tam = 45
        velocidad = random.uniform(3, 4.5) * dificultad
        puntaje = 7
    else:  # manzana
        tam = 35
        velocidad = random.uniform(4, 6) * dificultad
        puntaje = 5

    return Fruta(x, y, tipo, velocidad, tam, puntaje)


def atrapada_por_boca(fruta, boca_x, boca_y, boca_radio, boca_abierta):
    """
    Verifica si la fruta está cerca de la boca abierta.
    El rango efectivo de atrape aumenta con el tamaño de la fruta.
    """
    if not boca_abierta:
        return False

    # Rango efectivo: boca_radio + parte proporcional al tamaño de la fruta
    rango_efectivo = boca_radio + fruta.tam * 0.4

    distancia = ((fruta.x - boca_x) ** 2 + (fruta.y - boca_y) ** 2) ** 0.5
    return distancia <= rango_efectivo
