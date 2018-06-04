import RPi.GPIO as GPIO
from pynput.keyboard import Key, Controller
from time import sleep

k = Controller()

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

GPIO.setup(17, GPIO.IN)
GPIO.setup(22, GPIO.IN)
GPIO.setup(23, GPIO.IN)
GPIO.setup(27, GPIO.IN)

while 1:
    if GPIO.input(17) == 1:
        k.press('c')
        k.release('c')
        sleep(.5)
    elif GPIO.input(22) == 1:
        k.press('m')
        k.release('m')
        sleep(.5)
    elif GPIO.input(23) == 1:
        k.press('i')
        k.release('i')
        sleep(.5)
    elif GPIO.input(27) == 1:
        None
