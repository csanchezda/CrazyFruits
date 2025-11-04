# camera_utils.py

"""
Utilities para inicializar y liberar la cámara usando OpenCV.

Se centraliza aquí la configuración de la cámara (resolución por defecto)
para que el resto del proyecto pueda reutilizarla fácilmente.
"""

import cv2

def inicializar_camara(cam_index=0, ancho=1280, alto=720):
    """Abre la cámara por índice y establece resolución.

    Lanza RuntimeError si no es posible abrir la cámara.
    Devuelve el objeto VideoCapture.
    """
    cap = cv2.VideoCapture(cam_index)
    if not cap.isOpened():
        raise RuntimeError("No se pudo abrir la cámara")

    # Resolución más grande
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, ancho)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, alto)

    return cap

def liberar_camara(cap):
    """Libera recursos de la cámara y cierra ventanas OpenCV.

    Recibe el objeto VideoCapture abierto.
    """
    cap.release()
    cv2.destroyAllWindows()