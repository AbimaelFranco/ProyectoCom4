import RPi.GPIO as GPIO
from color_detector import detect_color_in_photo
import numpy as np

GPIO.setmode(GPIO.BCM)

pin_rojo = 26
pin_verde = 23
pin_azul = 24

GPIO.setup(pin_rojo, GPIO.OUT)
GPIO.setup(pin_verde, GPIO.OUT)
GPIO.setup(pin_azul, GPIO.OUT)

def turn_on_led(pin):
    GPIO.output(pin, GPIO. LOW)

def turn_off_led(pin):
    GPIO.output(pin, GPIO. HIGH)

def turn_off_leds():
    GPIO.output(pin_rojo, GPIO. HIGH)    
    GPIO.output(pin_verde, GPIO. HIGH)    
    GPIO.output(pin_azul, GPIO. HIGH)    

turn_off_leds()

while True:
    print("Menú:")
    print("1. Detectar color")
    print("2. Salir")
    choice = input("Seleccione una opción: ")
    
    if choice == '1':
        color_ranges = {
            "Rojo": (np.array([0, 100, 100]), np.array([10, 255, 255])),
            "Amarillo": (np.array([20, 100, 100]), np.array([30, 255, 255])),
            "Verde": (np.array([50, 100, 100]), np.array([85, 255, 255]))
        }
        result, predominant_color = detect_color_in_photo(color_ranges)
        print(result)
        print(type(result))

        if predominant_color == "Rojo":
            turn_on_led(pin_rojo)
            turn_off_led(pin_verde)
            turn_off_led(pin_azul)
        elif predominant_color == "Verde":
            turn_off_led(pin_rojo)
            turn_on_led(pin_verde)
            turn_off_led(pin_azul)
        elif predominant_color == "Amarillo":
            turn_on_led(pin_rojo)
            turn_on_led(pin_verde)
            turn_off_led(pin_azul)
        else:
            turn_off_leds

    elif choice == '2':
        print("Saliendo del programa.")
        GPIO.cleanup()
        break
    else:
        print("Opción no válida, intente nuevamente.")