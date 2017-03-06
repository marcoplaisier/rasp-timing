from pprint import pprint

import time

import logging

import sys
import wiringpi

CLOCK_LINE = 2
ENABLE_LINE = 3
DATA_LINE = 12

enabled = False
data = []

wiringpi.wiringPiSetup()
pins = [2, 3, 12, 13, 14]
for pin in pins:
    wiringpi.pinMode(pin, wiringpi.INPUT)


def clock_callback():
    global enabled
    if enabled:
        bit0 = wiringpi.digitalRead(DATA_LINE)
        bit1 = wiringpi.digitalRead(DATA_LINE)
        bit2 = wiringpi.digitalRead(DATA_LINE)
        if bit0 == bit1 == bit2:
            data.append(bit0)
        else:
            logging.info("ERROR ERROR ERROR")


def enable_callback():
    global enabled
    if not enabled and wiringpi.digitalRead(ENABLE_LINE) == wiringpi.HIGH:
        start = wiringpi.micros()
        enabled = True
        end = wiringpi.micros()
        logging.info('Enable clock callback in {} us'.format(end - start))
    elif enabled and wiringpi.digitalRead(ENABLE_LINE) == wiringpi.LOW:
        start = wiringpi.micros()
        enabled = False
        end = wiringpi.micros()
        logging.info('Disable clock callback in {} us'.format(end - start))
    else:
        pass


def get_bytes(bit_array=[]):
    if len(bit_array) % 8 != 0:
        bit_array.pop(0)
    if len(bit_array) % 8 != 0:
        bit_array.pop(0)

    bytes = []
    n = 0
    value = 0
    while bit_array:
        bit = bit_array.pop()
        value += bit * 2 ** n
        n += 1
        if n > 7:
            bytes.append(value)
            value = 0
            n = 0

    return bytearray(bytes[::-1])


def get_string(byte_array=[]):
    return str(byte_array, encoding='utf_8')


if __name__ == '__main__':
    logging.basicConfig(format='%(asctime)s %(message)s', level='INFO')
    start = wiringpi.micros()
    logging.info('Start at {}'.format(start))
    wiringpi.wiringPiISR(ENABLE_LINE, wiringpi.INT_EDGE_BOTH, enable_callback)
    wiringpi.wiringPiISR(CLOCK_LINE, wiringpi.INT_EDGE_RISING, clock_callback)
    end = wiringpi.micros()
    logging.info('Callbacks set in {} us'.format(end - start))
    while not enabled:
        # logging.info('Waiting for data')
        time.sleep(0.2)
    logging.info('Data ready')
    while enabled:
        # logging.info('Receiving data')
        time.sleep(0.1)
    delta = wiringpi.micros() - start
    logging.info('Data received in {} us'.format(delta))
    logging.info('Speed {} bps'.format(len(data)/delta*1000000))
    bytes_data = get_bytes(data)
    logging.info(bytes_data)
    s = get_string(bytes_data)
    logging.info(s)
    sys.exit(0)
