from pprint import pprint

import time

import logging
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
        logging.info((wiringpi.micros(), wiringpi.digitalRead(DATA_LINE)))


def enable_callback():
    global enabled
    if not enabled and wiringpi.digitalRead(ENABLE_LINE) == wiringpi.HIGH:
        start = wiringpi.micros()
        enabled = True
        end = wiringpi.micros()
        logging.info('\nEnable clock callback in {} us'.format(end-start))
    elif enabled and wiringpi.digitalRead(ENABLE_LINE) == wiringpi.LOW:
        start = wiringpi.micros()
        enabled = False
        end = wiringpi.micros()
        logging.info('\nDisable clock callback in {} us'.format(end - start))
    else:
        pass


if __name__ == '__main__':
    logging.basicConfig(format='%(asctime)s %(message)s', level='INFO')
    logging.info('Start at {}'.format(wiringpi.micros()))
    start = wiringpi.micros()
    wiringpi.wiringPiISR(ENABLE_LINE, wiringpi.INT_EDGE_BOTH, enable_callback)
    wiringpi.wiringPiISR(CLOCK_LINE, wiringpi.INT_EDGE_RISING, clock_callback)
    end = wiringpi.micros()
    logging.info('\nCallbacks set in {} us'.format(end-start))
    time.sleep(8)
