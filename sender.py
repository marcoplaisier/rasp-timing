import wiringpi

SLEEP_TIME = 100
CYCLES = 6
HIGH = 1
LOW = 0

wiringpi.wiringPiSetup()
pins = [2, 3, 12, 13, 14]
for pin in pins:
    wiringpi.pinMode(pin, wiringpi.OUTPUT)

counter = 0
pin = pins[0]
wiringpi.delay(1000)

while counter < CYCLES:
    wiringpi.digitalWrite(pin, HIGH)
    wiringpi.delayMicroseconds(SLEEP_TIME)
    wiringpi.digitalWrite(pin, LOW)
    wiringpi.delayMicroseconds(SLEEP_TIME)
    counter += 1

print('All done')