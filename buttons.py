import RPi.GPIO as GPIO
from pynput.keyboard import Key, Controller

k = Controller()

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

GPIO.setup(17, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
GPIO.setup(22, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
GPIO.setup(23, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
GPIO.setup(27, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)

while 1:
    if GPIO.input(17) == 1:
        k.press('c')
        k.release('c')
    elif GPIO.input(22) == 1:
        k.press('m')
        k.release('m')
    elif GPIO.input(23) == 1:
        k.press('i')
        k.release('i')
    elif GPIO.input(27) == 1:
        None
