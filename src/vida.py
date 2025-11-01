# vida.py
import cv2

class Vida:
    def __init__(self, total):
        self.total = total
        self.actual = total
        self.animaciones = []  # animaciones de corazones que laten antes de desaparecer

    def perder_vida(self):
        """Reduce una vida y lanza la animación del corazón perdido."""
        if self.actual > 0:
            indice_perdida = self.actual - 1
            self.animaciones.append({"indice": indice_perdida, "frame": 0})
            self.actual -= 1

    def reiniciar(self):
        """Restaura todas las vidas y limpia animaciones."""
        self.actual = self.total
        self.animaciones.clear()
