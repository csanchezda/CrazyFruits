# vida.py
"""
Módulo que encapsula la lógica sencilla de las vidas del jugador.

La clase `Vida` mantiene el número total de vidas, las actuales y listas
de animaciones a ejecutar cuando se pierde o gana una vida. No dibuja
por sí misma; las animaciones se consumen por `graphics.dibujar_vidas`.
"""

import cv2

class Vida:
    """Controla el contador de vidas y las animaciones asociadas.

    Atributos:
    - total: número inicial/máximo de vidas
    - actual: vidas restantes en la partida
    - animaciones: lista de animaciones de pérdida
    - animaciones_ganar: lista de animaciones de ganancia
    """
    def __init__(self, total):
        self.total = total
        self.actual = total
        self.animaciones = []  # animaciones de corazones que laten antes de desaparecer
        self.animaciones_ganar = []    # animaciones de vida ganada


    def perder_vida(self):
        """Reduce una vida y lanza la animación del corazón perdido.

        Agrega una entrada en `animaciones` que luego será procesada por
        el renderer para mostrar el efecto visual de la pérdida.
        """
        if self.actual > 0:
            indice_perdida = self.actual - 1
            self.animaciones.append({"indice": indice_perdida, "frame": 0})
            self.actual -= 1
            print("[VIDA] 1 vida perdida")


    def ganar_vida(self):
        """Incrementa las vidas y dispara la animación de ganancia."""
        self.actual += 1
        # Lanzamos animación de ganar vida en la posición de la nueva vida
        self.animaciones_ganar.append({"indice": self.actual - 1, "frame": 0})
        print("[VIDA] +1 vida ganada")

    def reiniciar(self):
        """Restaura todas las vidas y limpia animaciones para una nueva partida."""
        self.actual = self.total
        self.animaciones.clear()
        self.animaciones_ganar.clear()
