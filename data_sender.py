import logging

import sys
import wiringpi

SLEEP_TIME = 2500

logging.basicConfig(format='%(asctime)s %(message)s', level='INFO')

wiringpi.wiringPiSetup()
CLOCK_LINE = 2
ENABLE_LINE = 3
DATA_LINE = 12
pins = [2, 3, 12, 13, 14]
for pin in pins:
    wiringpi.pinMode(pin, wiringpi.OUTPUT)


def bits(number=0, num_bits=8):
    return [(number >> bit) & 1 for bit in range(num_bits - 1, -1, -1)]


def send_byte(byte=0b0):
    if byte > 0b11111111:
        raise ValueError('Byte {} is too large'.format(byte))
    for bit in bits(byte):
        wiringpi.digitalWrite(DATA_LINE, bit)
        wiringpi.digitalWrite(CLOCK_LINE, 1)
        wiringpi.delayMicroseconds(SLEEP_TIME)
        wiringpi.digitalWrite(CLOCK_LINE, 0)
        wiringpi.delayMicroseconds(SLEEP_TIME)


def send_data(data=''):
    b_data = bytes(source=data, encoding='utf-8')
    for byte in b_data:
        send_byte(byte)


if __name__ == '__main__':
    wiringpi.digitalWrite(ENABLE_LINE, 0)
    wiringpi.digitalWrite(DATA_LINE, 0)
    wiringpi.digitalWrite(CLOCK_LINE, 0)
    wiringpi.delay(3000)

    wiringpi.digitalWrite(ENABLE_LINE, 1)
    wiringpi.delay(8)

    data = """Lorem ipsum dolor sit amet, consectetur adipiscing elit. Proin a ultrices arcu, at faucibus augue. Proin vel erat nunc. Pellentesque egestas laoreet pulvinar. Praesent ullamcorper malesuada risus, at gravida diam tempor sed. Vivamus finibus interdum arcu, nec laoreet arcu consequat quis. Praesent pretium in erat a vestibulum. Aenean ultricies ut mauris vel tempus. Nam vel lorem ullamcorper, imperdiet tortor sit amet, porta enim. Mauris sit amet dui ultrices, aliquam magna a, pulvinar est. Maecenas cursus dapibus fermentum. Duis id velit a risus volutpat sagittis sed sagittis ligula. Morbi feugiat diam risus, nec aliquet felis aliquam ut."""
    send_data(data)
    b = bytes(data, encoding='utf-8')
    logging.info(b)

    wiringpi.digitalWrite(ENABLE_LINE, 0)
    wiringpi.digitalWrite(DATA_LINE, 0)
    wiringpi.digitalWrite(CLOCK_LINE, 0)

    logging.info('All done')
    sys.exit(0)
