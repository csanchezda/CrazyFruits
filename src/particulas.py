"""
Módulo de partículas sencillo usado para efectos visuales cuando se come una fruta.

Cada `Particula` tiene posición, velocidad (dx, dy) y una vida que decrece con el tiempo.
"""

import random

class Particula:
    """Partícula simple con movimiento lineal y vida finita.

    Se usa para representar pequeños destellos que aparecen al comer frutas.
    """
    def __init__(self, x, y, color, vida=15):
        self.x = x
        self.y = y
        self.color = color
        # Velocidad inicial aleatoria para dar variedad a las partículas
        self.dx = random.randint(-5, 5)
        self.dy = random.randint(-5, -1)
        self.vida = vida

    def mover(self):
        """Actualiza la posición y reduce la vida; cuando vida<=0 se descarta."""
        self.x += self.dx
        self.y += self.dy
        self.vida -= 1
