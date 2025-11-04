"""
Definición de tipos de frutas y metadatos asociados.

Cada miembro de `TipoFruta` contiene el nombre de archivo de la imagen,
un tamaño de referencia (tam), un rango de velocidad (vel_range) y el
valor de puntaje que otorga cuando se come.
"""

import os
from enum import Enum

ASSETS_DIR = os.path.join("assets", "icons/frutas")

class TipoFruta(Enum):
    APPLE = ("apple", 65, (4, 6), 6)
    BANANA = ("banana", 70, (3.5, 5), 6)
    CHERRY = ("cherry", 50, (5, 7), 10)
    LEMON = ("lemon", 55, (4.5, 6.5), 9)
    ORANGE = ("orange", 75, (3, 4.5), 5)
    PEAR = ("pear", 70, (3.5, 5), 6)
    STRAWBERRY = ("strawberry", 52, (5, 7), 10)
    RASPBERRY = ("raspberry", 50, (5, 7), 11)
    WATERMELON = ("watermelon", 110, (2, 3), 3)
    BOMB = ("bomb", 80, (3, 5), -15)
    MIX = ("mixFruta", 45, (5, 7), 0)

    def __init__(self, nombre_archivo, tam, vel_range, puntaje):
        # nombre_archivo: nombre del PNG en assets
        self.nombre_archivo = nombre_archivo
        self.tam = tam
        self.vel_range = vel_range
        self.puntaje = puntaje

    @property
    def ruta_imagen(self):
        """Ruta completa al archivo de imagen asociado al tipo de fruta."""
        return os.path.join(ASSETS_DIR, f"{self.nombre_archivo}.png")
