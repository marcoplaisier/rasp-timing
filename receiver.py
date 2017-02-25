import wiringpi

wiringpi.wiringPiSetup()
pins = [2, 3, 12, 13, 14]
for pin in pins:
    wiringpi.pinMode(pin, wiringpi.INPUT)

