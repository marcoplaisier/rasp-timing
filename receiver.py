from pprint import pprint

import time
import wiringpi

CLOCK_LINE = 2
ENABLE_LINE = 3
DATA_LINE = 12

enabled = False

wiringpi.wiringPiSetup()
pins = [2, 3, 12, 13, 14]
for pin in pins:
    wiringpi.pinMode(pin, wiringpi.INPUT)


def clock_callback():
    global enabled
    if enabled:
        print((wiringpi.micros(), wiringpi.digitalRead(DATA_LINE)))


def enable_callback():
    global enabled
    if not enabled:
        start = wiringpi.micros()
        enabled = True
        end = wiringpi.micros()
        print('\nEnable clock callback in {} us'.format(end-start))


if __name__ == '__main__':
    print('Start at {}'.format(wiringpi.micros()))
    start = wiringpi.micros()
    wiringpi.wiringPiISR(ENABLE_LINE, wiringpi.INT_EDGE_RISING, enable_callback)
    wiringpi.wiringPiISR(CLOCK_LINE, wiringpi.INT_EDGE_RISING, clock_callback)
    end = wiringpi.micros()
    print('\nCallbacks set in {} us'.format(end-start))
    time.sleep(8)
