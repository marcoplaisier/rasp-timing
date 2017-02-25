from pprint import pprint

import wiringpi

CYCLES = 3

wiringpi.wiringPiSetup()
pins = [2, 3, 12, 13, 14]
for pin in pins:
    wiringpi.pinMode(pin, wiringpi.INPUT)

data = []


def callback():
    data.append(wiringpi.micros())


pin = pins[0]
start_time = wiringpi.millis()
wiringpi.wiringPiISR(pin, wiringpi.INT_EDGE_RISING, callback)

while start_time + (CYCLES * 1000) > wiringpi.millis():
    wiringpi.delay(1000)

pprint(data[1:])
print(len(data[1:]))
