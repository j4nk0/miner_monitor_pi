import RPi.GPIO as G
from time import sleep

def restart(gpio_nr):
    G.setmode(G.BOARD)
    G.setup(gpio_nr, G.OUT, initial=G.HIGH)
    sleep(120)
    G.output(5, G.LOW)
    G.cleanup()

restart(5)
