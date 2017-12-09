import math
import random
import time

from RPi import GPIO as gpio

pin = [2, 4, 15, 13, 21, 25, 8, 5, 10, 16, 17, 27, 26, 24, 9, 12, 6, 20, 19, 14, 18, 11, 7, 23, 22]

by_y = [[pin[p] for p in row]
        for row in [[19, 22, 8, 4, 23], [17, 16, 24, 2, 13, 15], [3, 20], [1, 6, 14, 12, 7], [10], [9, 11, 5, 21], [18], [0]]]

def blink_randomly():
    while not (yield):
        p = random.choice(pin)
        gpio.output(p, 1 - gpio.input(p))
        time.sleep(0.1)

def blink_all():
    while not (yield):
        for p in pin:
            gpio.output(p, 1)
        time.sleep(0.1)
        for p in pin:
            gpio.output(p, 0)
        time.sleep(0.1)

def rain():
    while not (yield):
        for row in by_y[::-1]:
            for p in row:
                gpio.output(p, 1)
            time.sleep(0.3)
            for p in row:
                gpio.output(p, 0)
        

try:
    gpio.setmode(gpio.BCM)
    for (i, x) in enumerate(pin):
        print('set led={i} pin={x} to output'.format(i=i, x=x))
        gpio.setup(x, gpio.OUT)
        gpio.output(x, 0)

    while True:
        g = random.choice([blink_randomly, rain])
        print(g.__name__)
        g = g()
        try:
            t0 = time.time()
            while time.time() - t0 < 10:
                next(g)
            g.send(1)
        except StopIteration:
            pass
finally:
    for p in pin:
        gpio.output(p, 0)
    gpio.cleanup()
