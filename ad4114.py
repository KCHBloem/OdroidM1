import spidev
class AD4114:
 ID_REGISTER = 0x07
 COMM_REGISTER = 0x00
 CHANNEL_0_REGISTER = 0x10
 DATA_REGISTER = 0x04
 ADC_MODE_REGISTER = 0x01
 SETUP_REGISTER_0 = 0x20


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
  if (bytes == 2):
   return (received[1] << 8) | received[2]
  if (bytes == 3):
   return received[1] << 16 | received[2] << 8 | received[3]
   
 def read_ID_Register(self):
  return self.read_Register(self.ID_REGISTER, 2) 
 
 #Write
 
 def write(self, channel, data):
  message = [self.COMM_REGISTER | channel]
  data1 = (data>>8) & (0xFF)
  data2 = data & 0xFF
  message.append(data1)
  message.append(data2) 
  	
  self.spi.xfer2(message)
  
 def disable_channel(self, channel):
   channel = self.CHANNEL_0_REGISTER + channel
   self.write(channel, (self.read_Register(channel, 2) & 0x7FFF))	
   	
 def enable_channel(self, channel):
   channel = self.CHANNEL_0_REGISTER + channel
   self.write(channel, (self.read_Register(channel, 2) | 0x8000))
   	
 def read_channel(self, channel):
  return self.read_Register((self.CHANNEL_0_REGISTER + channel), 2)
 
 def set_channel_input(self, channel, data):
   channel = self.CHANNEL_0_REGISTER + channel
   self.write(channel, (self.read_Register(channel, 2) & 0xFC00))
   self.write(channel, (self.read_Register(channel, 2) | data))
 
 def read_data(self):
   return self.read_Register(self.DATA_REGISTER, 3)
   
 def read_adc_mode(self):
   return self.read_Register(self.ADC_MODE_REGISTER, 2)

 def set_adc_mode(self, Ref_EN, Sing_Cyc, Delay, Mode, Clock):
   data = (Ref_EN << 15) | (Sing_Cyc << 13) | (Delay << 8) | (Mode << 4) | (Clock << 2)
   self.write(self.ADC_MODE_REGISTER, data)
 
 def read_setup_configuration(self, number):
   reg = self.SETUP_REGISTER_0 + number;
   return self.read_Register(reg, 2)


 def set_setup_configuration(self, number, BI_UNIPOLAR, REFBUF_P, REFBUF_N, INBUF, REF_SEL):
  reg = self.SETUP_REGISTER_0 + number;
  data = (BI_UNIPOLAR << 12) | (REFBUF_P << 11) | (REFBUF_N << 10) | (INBUF << 8) | (REF_SEL << 4)
  self.write(reg, data)
 
 
