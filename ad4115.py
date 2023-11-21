import spidev
class AD4115:
 COMM_REGISTER = 0x00
 STATUS_REGISTER = 0x00
 ADC_MODE_REGISTER = 0x01
 INTERFACE_REGISTER = 0x02
 REG_CHECK_REGISTER = 0x03
 DATA_REGISTER = 0x04
 GPIO_REGISTER = 0x06
 ID_REGISTER = 0x07
 CHANNEL_0_REGISTER = 0x10
 SETUP_0_REGISTER = 0x20
 
 OFFSET_0_REGISTER = 0x30
 GAIN_0_REGISTER = 0x38


 def __init__(self, mode, speed):
  self.spi = spidev.SpiDev()
  self.spi.open(0,0)
  self.spi.max_speed_hz = speed
  self.mode = mode
  
 #Standard Reading Function
 def read_Register(self, reg, bytes):
  comms = [0x40 | reg]
  for x in range(bytes):
   comms.append(0x00)
  
  registerValue = self.spi.xfer2(comms)
  if (bytes == 2):
   return (registerValue[1] << 8) | registerValue[2]
  if (bytes == 3):
   return registerValue[1] << 16 | registerValue[2] << 8 | registerValue[3]
   
 #Standard Writing Function
 def write_Register(self, channel, data):
  comm = [self.COMM_REGISTER | channel]
  data1 = (data>>8) & (0xFF)
  data2 = data & 0xFF
  comm.append(data1)
  comm.append(data2) 
  	
  self.spi.xfer2(comm)
  
 #  R/W   NAME  REG    LENGTH    RESET
 # [READ] [ID] [0x07] [2-Bytes] [0x38Dx]
 # This function reads the ID of the device, it should always return 0x38DX where x can be anything
 def read_ID_Register(self):
  return self.read_Register(self.ID_REGISTER, 2) 
 
 def disableAllChannels(self):
  for channel in range(15):
   self.write_Register(self.CHANNEL_0_REGISTER + channel, (self.read_Register(self.CHANNEL_0_REGISTER + channel, 2) & ~(0x8000)))	

 def printAllChannels(self):
  for channel in range(15):
   print("Channel {}: 0x{}".format(channel, self.read_Register(self.CHANNEL_0_REGISTER + channel, 2)))
 

 def read_data(self):
  return self.read_Register(self.DATA_REGISTER, 3)
   
 def read_adc_mode(self):
   return self.read_Register(self.ADC_MODE_REGISTER, 2)

 def set_adc_mode(self, Ref_EN, Sing_Cyc, Delay, Mode, Clock):
   data = (Ref_EN << 15) | (Sing_Cyc << 13) | (Delay << 8) | (Mode << 4) | (Clock << 2)
   self.write_Register(self.ADC_MODE_REGISTER, data)
 
 
 
 class Channel:
  def __init__(self, adc, channel):
   self.adc = adc
   self.channel = channel
   self.register = self.adc.CHANNEL_0_REGISTER + self.channel
  
  def readChannel(self):
   return self.adc.read_Register(self.register, 2)
  
  def enableChannel(self):
   self.adc.write_Register(self.register, (self.adc.read_Register(self.register, 2) | 0x8000))

  def disableChannel(self):
   self.adc.write_Register(self.register, (self.adc.read_Register(self.register, 2) & ~(0x8000)))	
  
  def setInputs(self, pos, neg):
   pos = (int(pos) << 5)
   if (neg != 'VINCOM'):
    neg = (int(neg))
   else:
    neg = 0x10

   inputs = pos | neg
   #Write inverse of INPUT bits to clear input bits
   self.adc.write_Register(self.register, (self.adc.read_Register(self.register, 2) & ~(0x3FF)))
   self.adc.write_Register(self.register, (self.adc.read_Register(self.register, 2) | inputs))
  def useSetup(self, setup):
   self.adc.write_Register(self.register, (self.adc.read_Register(self.register, 2) & ~(0x7000)))
   self.adc.write_Register(self.register, (self.adc.read_Register(self.register, 2) | (setup << 12)))
 
 def set_channel_input(self, channel, data):
   channel = self.CHANNEL_0_REGISTER + channel
   self.write_Register(channel, (self.read_Register(channel, 2) & 0xFC00))
   self.write_Register(channel, (self.read_Register(channel, 2) | data))
 

 class Setup:
  def __init__(self, adc, setup):
   self.adc = adc
   self.setup = setup
   self.register = self.adc.SETUP_0_REGISTER + setup
   self.register_gain = self.adc.GAIN_0_REGISTER + setup
   self.register_offset = self.adc.OFFSET_0_REGISTER + setup
  
  def readSetup(self):
   return self.adc.read_Register(self.register, 2)
  
  def setGain(self, gain):
   self.adc.write_Register(self.register_gain, gain)

  def readGain(self):
   return self.adc.read_Register(self.register_gain, 3)
  
  def readOffset(self):
   return self.adc.read_Register(self.register_offset, 3)

  def setOffset(self, offset):
   self.adc.write_Register(self.register_offset, offset)

  def setBipolarOutput(self):
   self.adc.write_Register(self.register, self.adc.read_Register(self.register, 2) | (0x01 << 12))

  def setUnipolarOutput(self):
   self.adc.write_Register(self.register, self.adc.read_Register(self.register, 2) & ~(0x01 << 12))
  
  def setRefBufState(self, refbuf_p, refbuf_n):
   self.adc.write_Register(self.register, self.adc.read_Register(self.register, 2) & ~(0x03 << 10))
   self.adc.write_Register(self.register, self.adc.read_Register(self.register, 2) | (((refbuf_p << 1) | (refbuf_n)) << 10))
  
  def enableInputBuffer(self):
   self.adc.write_Register(self.register, self.adc.read_Register(self.register, 2) | (0x03 << 8))
   
  def disableInputBuffer(self):
   self.adc.write_Register(self.register, self.adc.read_Register(self.register, 2) & ~(0x03 << 8))

  def selectReference(self, ref):
   self.adc.write_Register(self.register, self.adc.read_Register(self.register, 2) & ~(0x30))
   if (ref == "External"):
    self.adc.write_Register(self.register, 0x00 << 4)
   elif (ref == "Internal"):
    self.adc.write_Register(self.register, 0x02 << 4)
   elif (ref == "Analog"):
    self.adc.write_Register(self.register, 0x03 << 4)
   else:
    print("[ERROR] - Unknown reference please select: 'External', 'Internal' or 'Analog'")

