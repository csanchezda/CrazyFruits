import cv2

def dibujar_cesta(frame, basket_x, basket_y, basket_width=120, basket_height=25):
    cv2.rectangle(frame, (basket_x, basket_y), (basket_x + basket_width, basket_y + basket_height), (0, 255, 0), -1)

def dibujar_face(frame, x, y, w, h):
    face_center_x = x + w // 2
    cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 150, 0), 2)
    cv2.line(frame, (face_center_x, 0), (face_center_x, frame.shape[0]), (0, 255, 255), 1)
    return face_center_x
