import cv2
import numpy as np
from picamera2 import Picamera2, Preview

def detect_color_in_video(color_ranges):
    # Configurar la cámara
    picam2 = Picamera2()
    config = picam2.create_preview_configuration(main={"format": "XRGB8888", "size": (640, 480)})
    picam2.configure(config)
    picam2.start()

    while True:
        # Capturar un frame de la cámara
        frame = picam2.capture_array()
        
        # Girar la imagen 180°
        frame = cv2.rotate(frame, cv2.ROTATE_180)

        # Convertir el frame a espacio de color HSV
        hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        
        for color_name, (lower_color, upper_color) in color_ranges.items():
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
                
                # Obtener el momento del contorno para encontrar el centro
                M = cv2.moments(largest_contour)
                if M["m00"] != 0:
                    cX = int(M["m10"] / M["m00"])
                    cY = int(M["m01"] / M["m00"])
                    # Dibujar el nombre del color en el centro del contorno
                    cv2.putText(frame, color_name, (cX - 20, cY - 20), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
        
        # Mostrar el frame original
        cv2.imshow("Frame Original", frame)
        
        # Romper el bucle si se presiona la tecla 'q'
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Cerrar las ventanas
    cv2.destroyAllWindows()
    picam2.stop()

if __name__ == "__main__":
    # Especificar los rangos de colores en HSV
    color_ranges = {
        "Rojo": (np.array([170, 100, 100]), np.array([179, 255, 255])),
        "Amarillo": (np.array([20, 100, 100]), np.array([30, 255, 255])),
        "Verde": (np.array([70, 100, 100]), np.array([80, 255, 255]))
    }

    detect_color_in_video(color_ranges)
