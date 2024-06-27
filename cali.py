from gpiozero import Servo, AngularServo
from time import sleep
from gpiozero.pins.pigpio import PiGPIOFactory

factory = PiGPIOFactory()

correction = 0.45
minPW = (1-correction)/1000
maxPW = (2+correction)/1000

servo2 = AngularServo(6, min_angle=-90, max_angle=90, min_pulse_width=minPW, max_pulse_width=maxPW, pin_factory=factory)

while True:
    print("Minimo:")
    servo2.min()
    sleep(2)
    print("Medio:")
    servo2.mid()
    sleep(2)
    print("Maximo:")
    servo2.max()
    sleep(2)