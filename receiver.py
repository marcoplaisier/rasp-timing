from pprint import pprint

import wiringpi

CYCLES = 40

wiringpi.wiringPiSetup()
pins = [2, 3, 12, 13, 14]
for pin in pins:
    wiringpi.pinMode(pin, wiringpi.INPUT)

data = []
pin = pins[0]
start_time = wiringpi.millis()
while start_time + (CYCLES * 1000) > wiringpi.millis():
    value = wiringpi.digitalRead(pin)
    data.append((wiringpi.millis(), value))
    wiringpi.delay(10)

pprint(data)