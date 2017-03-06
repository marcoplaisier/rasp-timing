from pprint import pprint

import time

import logging
import wiringpi
from os import system

ENABLE_LINE = 11 # INT
ACK = 13
DATA_LINE = 15 # DA
CLOCK_LINE = 16 #CL

enabled = False

wiringpi.wiringPiSetup()
input_pins = [x for x in range(1, 31) if x not in [20]]
logging.info("Initializing pins")
# for pin in input_pins:
#     wiringpi.pinMode(pin, wiringpi.INPUT)
#     time.sleep(0.5)
logging.info("Pins initialized")

# output_pins = [ACK]
# for pin in output_pins:
#     wiringpi.pinMode(pin, wiringpi.OUTPUT)


def clock_callback():
    global enabled
    if enabled:
        logging.info((wiringpi.micros(), wiringpi.digitalRead(DATA_LINE)))


def enable_callback():
    logging.info('Interrupt')
    # global enabled
    # if not enabled and wiringpi.digitalRead(ENABLE_LINE) == wiringpi.LOW:
    #     start = wiringpi.micros()
    #     enabled = True
    #     wiringpi.digitalWrite(ACK, wiringpi.HIGH)
    #     end = wiringpi.micros()
    #     logging.info('Enable clock callback in {} us'.format(end-start))
    # elif enabled and wiringpi.digitalRead(ENABLE_LINE) == wiringpi.HIGH:
    #     start = wiringpi.micros()
    #     enabled = False
    #     wiringpi.digitalWrite(ACK, wiringpi.LOW)
    #     end = wiringpi.micros()
    #     logging.info('Disable clock callback in {} us'.format(end - start))
    # else:
    #     pass


if __name__ == '__main__':
    logging.basicConfig(format='%(asctime)s %(message)s', level='INFO')
    logging.info('Start at {}'.format(wiringpi.micros()))
    start = wiringpi.micros()
    for pin in input_pins:
        logging.info('Start pin {}'.format(pin))
        wiringpi.wiringPiISR(pin, wiringpi.INT_EDGE_BOTH, enable_callback)
        time.sleep(1)
        logging.info('End pin {}'.format(pin))

    # wiringpi.wiringPiISR(ENABLE_LINE, wiringpi.INT_EDGE_BOTH, enable_callback)
    # wiringpi.wiringPiISR(CLOCK_LINE, wiringpi.INT_EDGE_RISING, clock_callback)
    end = wiringpi.micros()
    logging.info('Callbacks set in {} us'.format(end-start))
    time.sleep(60)
