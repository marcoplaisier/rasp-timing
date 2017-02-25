import wiringpi
import time

SLEEP_TIME = 1
CYCLES = 10
HIGH = 1
LOW = 0

wiringpi.wiringPiSetup()
pins = [2, 3, 12, 13, 14]
for pin in pins:
    wiringpi.pinMode(pin, wiringpi.OUTPUT)

counter = 0
pin = pins[0]
time.sleep(2)

while counter < CYCLES:
    wiringpi.digitalWrite(pin, HIGH)
    time.sleep(SLEEP_TIME)
    wiringpi.digitalWrite(pin, LOW)
    time.sleep(SLEEP_TIME)
    counter += 1