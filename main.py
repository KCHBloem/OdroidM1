#!/usr/bin/env python
 
import odroid_wiringpi as wpi
import time
from ad4114 import AD4114 


wpi.wiringPiSetup()
wpi.pinMode(0, 1)

adc = AD4114(0b11, 25000)

print(hex(adc.read_ID_Register()))

while True:
    
    wpi.digitalWrite(0, 1)
    time.sleep(1)
    wpi.digitalWrite(0, 0)
    time.sleep(1)
    
    
    

    
