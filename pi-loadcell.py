# pi-loadcell.py
# HX711 datasheet: https://www.digikey.com/htmldatasheets/production/1836471/0/0/1/hx711.html

import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)  # set up BCM GPIO numbering 

class HX711LoadCell:
  
  
  # pd_sck  | digital input   | GPIO pin for power down control (high active) and serial clock input
  # dout    | digital output  | GPIO pin for serial data output 
  def __init__(self, pd_sck, dout, gain=128, bitMSB=True, byteMSB=True, channelSelect='A'):
    
    self.pd_sck = pd_sck
    self.dout = dout
    self.gain = gain
    
    # Set True for MSB format, False for LSB format
    self.bitMSB = bitMSB
    self.byteMSB = byteMSB
    
    # HX711 has two input channels, A & B
    self.channelSelect = channelSelect
    
    # Initialize GPIO
    GPIO.setup(self.pd_sck, GPIO.IN)
    GPIO.setup(self.dout, GPIO.OUT)

  
  
  # Set AD amplifier gain. 32, 64, or 128 (default)
  def setGain(self, gain):
    
    self.gain = gain
  
  
  
  # Get AD amplifier gain. 32, 64, or 128 (default)
  def getGain(self):
    
    return self.gain
  
  
  
  # Set channel select
  def setChannelSelect(self, channel):
    
    self.channelSelect = channel
    
    
    
  # Get current channel select
  def setChannelSelect(self):
    
    return self.channelSelect
    
   
  
  # Pulse HX711 clock. Each PD_SCK pulse shifts out one bit, starting with the MSB bit first
  def pulseClock(self):
    
    GPIO.output(self.pd_sck, True)
    GPIO.output(self.pd_sck, False)
    
  
  
  # Read input on DOUT pin, and convert from bool to integer
  def readDOUT(self):
    
    return int(GPIO.input(self.dout))
  
  
  
  # Check dout pin for falling edge
  def isCommBusy(self):
    
    return GPIO.input(self.dout) == 0
  
  
  
  # To read next bit, pulse pd_sck clock pin, and read input from DOUT pin
  def readBit(self):
    
    self.pulseClock()
    return self.readDOUT()
  
  
  
  # Each PD_SCK pulse shifts out one bit, starting with the MSB bit first, until all 24 bits are 
  # shifted out. The 25th pulse at PD_SCK input will 
  # pull DOUT pin back to high
  def readByte(self):
    
    # Initialize variable for storing and shifting read bit values
    readByte = int(0)
    
    # Iterate through each bit in byte
    for i in range(8):
      
      # Check format for MSB or LSB to deterne if left or right shifting of bits
      if self.bitMSB:
        
        readByte <<= 1
        readByte |= self.readBit()
      else:
        
        readByte >>= 1
        readByte |= self.readBit() * 0b10000000
      
      return readByte
    
    
    
    # Compacts array of bytes into single value
    def compactBytes(self, byteArray):
      
      numBytes = len(byteArray)
      startShift = (numBytes * 8) - 8 # For left shift of bits in byte array
      byteValue = 0b0
      
      for i in range(numBytes)
      
        byteValue |= (byteArray[i] << startShift)
        startShift -= 8
        
      return byteValue
      
    # Read 3 bytes from DOUT for 24 Bits of data from MX711
    # Returns int value
    def read24Bit(self):
      
      # variable for storing read byte data from DOUT
      dataBytes = []
      
      # Read 3 bytes from DOUT and store in array
      for i in range (3)
        
        dataBytes.append(self.readByte())
      
      # If MSB byte format, reverse order of bytes in array
      if self.byteMSB:
          
          dataBytes.reverse()
    
      return self.compactBytes(dataBytes)
    
    
    # When PD_SCK pin changes from low to high 
    # and stays at high for longer than 60µs, HX711 
    # enters power down mode
    def powerDown(self):
      
      # Toggle PK_SCK pin to high
      GPIO.output(self.pk_sck, False)
      GPIO.output(self.pk_sck, True)
      
      
     
    # Powers on HX711 chip set. On power up, gain is automatically reset to 128. 
    # Reset gain and channel select to stored values on startup.
    def powerUp(self):
      
      # Write PK_SCK pin low
      GPIO.output(self.pk_sck, False)
      
      
      
      
    
    