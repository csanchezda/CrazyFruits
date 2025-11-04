"""
Módulo de manejo de objetos `Fruta` y funciones de utilidad.

Contiene la clase `Fruta` que encapsula posición, velocidad, tamaño y
la imagen asociada que se dibuja en pantalla. Además hay utilidades para
generar frutas aleatorias y detectar si una fruta ha sido atrapada por la boca.
"""

import random
import os
import cv2
from tipo_fruta import TipoFruta

class Fruta:
    """Representa una fruta que cae en la pantalla.

    Atributos:
    - x, y: posiciones (float/int)
    - tipo: miembro de `TipoFruta` (contiene metadatos como ruta de imagen)
    - velocidad: velocidad vertical de caída
    - tam: tamaño de referencia para dibujar/colisiones
    - puntaje: valor que otorga cuando se come
    - imagen: imagen redimensionada (si existe) con posible canal alfa
    """
    def __init__(self, x, y, tipo: TipoFruta, velocidad, tam, puntaje):
        self.x = x
        self.y = y
        self.tipo = tipo # 'sandia', 'platano', 'manzana', etc.
        self.velocidad = velocidad
        self.tam = tam
        self.puntaje = puntaje

        # Intentar cargar la imagen asociada al tipo de fruta.
        ruta = tipo.ruta_imagen
        if os.path.exists(ruta):
            img = cv2.imread(ruta, cv2.IMREAD_UNCHANGED)
            if img is not None:
                h, w = img.shape[:2]
                escala = self.tam / max(h, w)
                new_w, new_h = int(w * escala), int(h * escala)
                self.imagen = cv2.resize(img, (new_w, new_h), interpolation=cv2.INTER_AREA)

            else:
                print(f"[WARN] No se pudo leer la imagen: {ruta}")
                self.imagen = None
        else:
            print(f"[WARN] Imagen no encontrada: {ruta}")
            self.imagen = None

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
    y = -40

    tipo = random.choice(list(TipoFruta))  # elegimos una fruta aleatoria
    vel_min, vel_max = tipo.vel_range
    velocidad = random.uniform(vel_min, vel_max) * dificultad
    puntaje = tipo.puntaje

    return Fruta(x, y, tipo, velocidad, tipo.tam, puntaje)


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

