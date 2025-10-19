import cv2

def inicializar_camara(cam_index=0):
    cap = cv2.VideoCapture(cam_index)
    if not cap.isOpened():
        raise RuntimeError("No se pudo abrir la cámara")
    return cap

def liberar_camara(cap):
    cap.release()
    cv2.destroyAllWindows()