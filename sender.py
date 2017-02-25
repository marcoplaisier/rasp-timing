import wiringpi

SLEEP_TIME = 10000
CYCLES = 6
HIGH = 1
LOW = 0

wiringpi.wiringPiSetup()
CLOCK_LINE = 2
ENABLE_LINE = 3
DATA_LINE = 12
pins = [2, 3, 12, 13, 14]
for pin in pins:
    wiringpi.pinMode(pin, wiringpi.OUTPUT)

if __name__ == '__main__':
    counter = 0
    wiringpi.digitalWrite(ENABLE_LINE, 0)
    wiringpi.delay(3000)
    wiringpi.digitalWrite(DATA_LINE, 0)
    wiringpi.digitalWrite(CLOCK_LINE, 0)
    wiringpi.delay(1000)

    wiringpi.digitalWrite(ENABLE_LINE, 1)
    wiringpi.delay(2)

    for i in range(5):
        wiringpi.digitalWrite(DATA_LINE, 1)
        wiringpi.delayMicroseconds(1000)
        wiringpi.digitalWrite(CLOCK_LINE, 1)
        wiringpi.delayMicroseconds(SLEEP_TIME)
        wiringpi.digitalWrite(CLOCK_LINE, 0)
        wiringpi.digitalWrite(DATA_LINE, 0)
        wiringpi.delayMicroseconds(SLEEP_TIME)

        wiringpi.digitalWrite(DATA_LINE, 0)
        wiringpi.delayMicroseconds(1000)
        wiringpi.digitalWrite(CLOCK_LINE, 1)
        wiringpi.delayMicroseconds(SLEEP_TIME)
        wiringpi.digitalWrite(CLOCK_LINE, 0)
        wiringpi.digitalWrite(DATA_LINE, 0)
        wiringpi.delayMicroseconds(SLEEP_TIME)

    wiringpi.digitalWrite(ENABLE_LINE, 0)
    wiringpi.digitalWrite(DATA_LINE, 0)
    wiringpi.digitalWrite(CLOCK_LINE, 0)

    print('All done')
