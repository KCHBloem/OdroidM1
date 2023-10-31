#!/usr/bin/env python
 
import odroid_wiringpi as wpi
import time
from ad4114 import AD4114 


vref = 2.5
n = 24

wpi.wiringPiSetup()
wpi.pinMode(0, 1)

adc = AD4114(0b11, 25000)

print(hex(adc.read_ID_Register()))
adc.set_adc_mode(1, 1, 7, 0, 0)
adc.set_setup_configuration(0, 1, 0, 0, 0, 2)

for x in range(15):
 adc.disable_channel(x)
 
adc.enable_channel(15)
adc.set_channel_input(15, 16)
print(adc.read_channel(15))






while True:
    code = adc.read_data()

    vin = (((code / (2**(n-1))) - 1) * vref * 10)
    print(vin)
    wpi.digitalWrite(0, 1)
    time.sleep(1)
    wpi.digitalWrite(0, 0)
    time.sleep(1)
    
    
    

    
