import os
import cv2

def cargar_cascades():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    mouth_cascade = cv2.CascadeClassifier(os.path.join(script_dir, "haarcascade_mcs_mouth.xml"))
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
    if mouth_cascade.empty() or face_cascade.empty():
        raise RuntimeError("No se pudieron cargar los cascades")
    return face_cascade, mouth_cascade

def detectar_boca(face_roi_gray, mouth_cascade):
    mouths = mouth_cascade.detectMultiScale(face_roi_gray, 1.5, 11)
    return len(mouths) == 0  # True si boca abierta
