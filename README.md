# rasp-timing
Exploring serial communication via GPIO

# Setup
Connect one or more GPIO pins on two Raspberry Pi.
Use a breadboard! Take care to put a 1K resistor in between to avoid a shortcircuit. Don't use the 5V or 3V3 pin. Do 
connect on ground pin on each Raspberry to a common ground. Connect both Rasperries to a bridge/router with an Ethernet 
cable or through Wifi if you have the new ones. 
Use a separate computing device as a manager. This avoids duplicate monitors, keyboards, mouses, etc.

# Installation
1. Burn two new Raspbian image to SD cards
2. On both images, place a file with name ssh on the image to enable SSH
3. Put the SD cards in the Raspberries

# Run
On the manager computing device, run main.py. This will take care of logging into the two Raspberries, setting up the 
code, running the code, and collecting the output.  