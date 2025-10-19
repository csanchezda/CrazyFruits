import cv2
from detectors import cargar_cascades
from camera_utils import inicializar_camara
from game import CrazyBasketGame

def main():
    face_cascade, mouth_cascade = cargar_cascades()
    cap = inicializar_camara()

    ret, frame = cap.read()
    frame_height, frame_width = frame.shape[:2]

    game = CrazyBasketGame(face_cascade, mouth_cascade, frame_width, frame_height)

    print("Presiona 'q' para salir.")
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        frame = game.procesar_frame(frame)
        cv2.imshow("CrazyBasket - Fase 2", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
