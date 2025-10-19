import random
import cv2

class Particula:
    def __init__(self, x, y, color, vida=15):
        self.x = x
        self.y = y
        self.color = color
        self.dx = random.randint(-5, 5)
        self.dy = random.randint(-5, -1)
        self.vida = vida

    def mover(self):
        self.x += self.dx
        self.y += self.dy
        self.vida -= 1

    def dibujar(self, frame):
        if self.vida > 0:
            cv2.circle(frame, (self.x, self.y), 3, self.color, -1)
