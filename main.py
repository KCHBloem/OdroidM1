#!/usr/bin/env python
 
import odroid_wiringpi as wpi
import time
import math
import json
from ad4115 import AD4115 
import csv




vref = 2.5
n = 24

thermistor_coefficient_A = 0.001125188066
thermistor_coefficient_B = 0.0002347201562
thermistor_coefficient_C = 0.00000008572176636


def steinhart(A, B, C, Resistance):
 return ((1/(A+(B*math.log(Resistance)) + (C * ((math.log(Resistance))**3)))) - 273.15)

wpi.wiringPiSetup()
wpi.pinMode(0, 1)

adc = AD4115(0b11, 10000000)

print(hex(adc.read_ID_Register()))
adc.disableAllChannels()
#adc.printAllChannels()


ch0 = adc.Channel(adc, 0)
ch0.setInputs('1', '0')
ch0.useSetup(0)
ch0.enableChannel()

setup0 = adc.Setup(adc, 0)
setup0.selectReference('Internal')
setup0.setRefBufState(1, 1)
setup0.enableInputBuffer()
setup0.setUnipolarOutput()
setup0.setGain(0x50000) # Default Gain
setup0.setOffset(0x800000) # Default Offset

adc.set_adc_mode(1, 0, 7, 0, 3)

print(hex(ch0.readChannel()))


samples = 0
filenumber = 0

header = ['ADC Value', 'Voltage', 'Resistance', 'Temperature']

rows = []
t0 = time.time()
while True:
    code = adc.read_data()
    #voltage = (code/(2**(n))) * vref * 10
     #resistance = ((5 - voltage) * 10000) / voltage
     #temperature = steinhart(thermistor_coefficient_A, thermistor_coefficient_B, thermistor_coefficient_C, resistance)
      #print("ADC Value: {} | Voltage: {:.4f} | Resistance: {:.4f} | Temperature: {:.4f}".format(code,voltage, resistance, temperature))
     #data = [code, voltage, resistance, temperature]
    data = [code]
    rows.append(data)
    samples +=1
    if (samples >= 100000):
     samples = 0
     duration = time.time() - t0
     t0 = time.time()
     filenumber += 1
     with open('data_{}'.format(filenumber), 'w') as f:
      write = csv.writer(f)
      write.writerow(header)
      write.writerows(rows)
      print("saved to file, 100k samples took {}, samplerate = {}".format(duration, 100000/duration))
      rows.clear()

    #wpi.digitalWrite(0, 1)
    #time.sleep(0.1)
    #wpi.digitalWrite(0, 0)
    #time.sleep(0.1)
    
    
    

    


#with open("../React-Dashboard/build/data.json", "r") as file:
 #      data = json.load(file)
  #    for item in data:
   #    if "TemperatureData" in item:
    #    for sensor_data in item["TemperatureData"]:
     #    if "Sensor 1" in sensor_data:
      #    sensor_data["Sensor 1"] = "{:.2f}".format(temperature)
      #with open("../React-Dashboard/build/data.json", "w") as file:
      # json.dump(data, file, indent=4)
