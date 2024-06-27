import cv2
import numpy as np
from picamera2 import Picamera2, Preview

def detect_color_in_video(lower_color, upper_color):
    # Capturar video desde la cámara
    # cap = cv2.VideoCapture(0)  # 0 es el índice de la cámara por defecto
    picam2 = Picamera2()
    config = picam2.create_preview_configuration(main={"format": "XRGB8888", "size": (640, 480)})
    picam2.configure(config)
    picam2.start()

    # if not cap.isOpened():
    #     print("Error: No se pudo abrir la cámara.")
    #     return

    while True:
        # Leer un frame de la cámara
        frame = picam2.capture_array()
        # if not ret:
            # print("Error: No se pudo leer el frame.")
            # break

        # Convertir el frame a espacio de color HSV
        hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        # Crear una máscara con el rango de colores especificado
        mask = cv2.inRange(hsv_frame, lower_color, upper_color)

        # Aplicar la máscara al frame original
        result_frame = cv2.bitwise_and(frame, frame, mask=mask)

        # Mostrar el frame original y el frame resultante
        cv2.imshow("Frame Original", frame)
        cv2.imshow("Color Detectado", result_frame)

        # Romper el bucle si se presiona la tecla 'q'
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Liberar la captura y cerrar las ventanas
    # cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    # Especificar el rango de colores en HSV
    # Por ejemplo, para detectar el color rojo:
    lower_red = np.array([0, 120, 70])
    upper_red = np.array([10, 255, 255])

    detect_color_in_video(lower_red, upper_red)
