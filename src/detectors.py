# detectors.py

"""
Herramientas para cargar clasificadores Haar Cascade y para detectar
si la boca está abierta a partir de una ROI de la cara en escala de grises.
"""

import os
import cv2

def cargar_cascades():
    """Carga los clasificadores necesarios (cara y boca) y los devuelve.

    Lanza RuntimeError si alguno no puede cargarse.
    """
    script_dir = os.path.dirname(os.path.abspath(__file__))
    mouth_cascade = cv2.CascadeClassifier(os.path.join(script_dir, "haarcascade_mcs_mouth.xml"))
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
    if mouth_cascade.empty() or face_cascade.empty():
        raise RuntimeError("No se pudieron cargar los cascades")
    return face_cascade, mouth_cascade

def detectar_boca(face_roi_gray, mouth_cascade):
    """Devuelve True si parece que la boca está abierta en la ROI.

    La heurística usada invierte la lógica del cascade (detectMultiScale
    devuelve regiones con probabilidad de encontrar la boca cerrada), por eso
    aquí se compara la longitud del resultado.
    """
    mouths = mouth_cascade.detectMultiScale(face_roi_gray, 1.5, 11)
    return len(mouths) == 0  # True si boca abierta
