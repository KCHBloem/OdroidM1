import spidev
class AD4114:
 ID_REGISTER = 0x07


 def __init__(self, mode, speed):
  self.spi = spidev.SpiDev()
  self.spi.open(0,0)
  self.spi.max_speed_hz = speed
  self.mode = mode
 
 def read_Register(self, reg, bytes):
  data = [0x40 | reg]
  for x in range(bytes):
   data.append(0x00)
  
  received = self.spi.xfer2(data)
  return (received[1] << 8) | received[2]

 def read_ID_Register(self):
  return self.read_Register(self.ID_REGISTER, 2) 
 
  
