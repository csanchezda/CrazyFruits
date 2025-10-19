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

    def dibujar(self, frame, x=20, y=20):
        # Dibujar corazones pequeños como representación de vidas
        for i in range(self.actual):
            cv2.circle(frame, (x + i*30, y), 10, (0, 0, 255), -1)
        # Opcional: dibujar número de vidas
        cv2.putText(frame, f"{self.actual}/{self.total}", (x, y + 40),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
