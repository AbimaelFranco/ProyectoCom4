from gpiozero import AngularServo
from time import sleep
from gpiozero.pins.pigpio import PiGPIOFactory

#Use before run this script the next command in shell "sudo pigpiod"
factory = PiGPIOFactory()

#Factor of correction in width pulse to use all angle avaible
correction = 0.45
minPW = (1-correction)/1000
maxPW = (2+correction)/1000 

#Time between move 1 grade
step_time = 0.025
joystick_speed = 1

#Configuration of all servos
servo1 = AngularServo(14, min_angle=-90, max_angle=90, min_pulse_width=minPW, max_pulse_width=maxPW, pin_factory=factory)

angulo1 = 0

def Ctrl_servo1(posicion, angulo):
    while True:
        if abs(angulo) <= 90:
            posicion = angulo
            servo1.angle = posicion
            return(posicion)
        else:
            # print(Fore.RED + "El angulo para este servo uno solo puede estar entre -15 a 15")
            return(posicion)
        

while True:        

    # opcion = int(input("Selecciona la accion a realizar: \n1. mover \n"))

    # if opcion ==1:
    tiempo = float(input("tiempo: "))
    print("---------------------------------------------")
    if tiempo > 0:
        angulo1 = Ctrl_servo1(angulo1, 90)
    elif tiempo < 0:
        angulo1 = Ctrl_servo1(angulo1, -90)

    sleep(abs(tiempo))
    angulo1 = Ctrl_servo1(angulo1, 0)
    # else:
    #     print("Seleccione otra opcion")
