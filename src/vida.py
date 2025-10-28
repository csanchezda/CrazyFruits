# vida.py

import cv2

class Vida:
    def __init__(self, total=3):
        self.total = total
        self.actual = total

    def perder_vida(self):
        if self.actual > 0:
            self.actual -= 1

    def reiniciar(self):
        self.actual = self.total
