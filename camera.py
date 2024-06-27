import cv2
import numpy as np
from picamera2 import Picamera2, Preview

def detect_color_in_video(lower_color, upper_color):
    # Configurar la cámara
    picam2 = Picamera2()
    config = picam2.create_preview_configuration(main={"format": "XRGB8888", "size": (640, 480)})
    picam2.configure(config)
    picam2.start()

    while True:
        # Capturar un frame de la cámara
        frame = picam2.capture_array()
        
        # Convertir el frame a espacio de color HSV
        hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        
        # Crear una máscara con el rango de colores especificado
        mask = cv2.inRange(hsv_frame, lower_color, upper_color)
        
        # Encontrar contornos en la máscara
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        # Si se encuentran contornos, dibujar el contorno más grande
        if contours:
            # Encontrar el contorno con el área más grande
            largest_contour = max(contours, key=cv2.contourArea)
            
            # Dibujar el contorno más grande en el frame original
            cv2.drawContours(frame, [largest_contour], -1, (0, 255, 0), 2)
        
        # Mostrar el frame original y el frame resultante
        cv2.imshow("Frame Original", frame)
        cv2.imshow("Color Detectado", cv2.bitwise_and(frame, frame, mask=mask))
        
        # Romper el bucle si se presiona la tecla 'q'
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Cerrar las ventanas
    cv2.destroyAllWindows()
    picam2.stop()

if __name__ == "__main__":
    # Especificar el rango de colores en HSV
    # Por ejemplo, para detectar el color rojo:
    lower_red = np.array([170, 100, 100])
    upper_red = np.array([179, 255, 255])

    detect_color_in_video(lower_red, upper_red)
