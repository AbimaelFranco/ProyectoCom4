import cv2
import numpy as np
from picamera2 import Picamera2

def detect_dominant_color_in_image(color_ranges):
    # Configurar la cámara
    picam2 = Picamera2()
    config = picam2.create_still_configuration(main={"format": "XRGB8888", "size": (640, 480)})
    picam2.configure(config)
    picam2.start()
    
    # Capturar una imagen de la cámara
    frame = picam2.capture_array()
    
    # Girar la imagen 180°
    frame = cv2.rotate(frame, cv2.ROTATE_180)

    # Convertir el frame a espacio de color HSV
    hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    
    # Diccionario para contar los píxeles de cada color
    color_count = {color_name: 0 for color_name in color_ranges}
    
    for color_name, (lower_color, upper_color) in color_ranges.items():
        # Crear una máscara con el rango de colores especificado
        mask = cv2.inRange(hsv_frame, lower_color, upper_color)
        
        # Contar el número de píxeles dentro del rango de color
        color_count[color_name] = cv2.countNonZero(mask)
    
    # Encontrar el color con el mayor número de píxeles
    dominant_color = max(color_count, key=color_count.get)
    
    # Imprimir el color dominante
    print(f"El color dominante es: {dominant_color}")
    
    # Mostrar la imagen capturada
    cv2.imshow("Imagen Capturada", frame)
    
    # Esperar a que se cierre la ventana
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    picam2.stop()

if __name__ == "__main__":
    # Especificar los rangos de colores en HSV
    color_ranges = {
        "Rojo": (np.array([170, 100, 100]), np.array([179, 255, 255])),
        "Amarillo": (np.array([20, 100, 100]), np.array([30, 255, 255])),
        "Verde": (np.array([70, 100, 100]), np.array([80, 255, 255]))
    }

    detect_dominant_color_in_image(color_ranges)
