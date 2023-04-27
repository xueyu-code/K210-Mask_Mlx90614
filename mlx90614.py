
#=======================测温=====================#
from machine import I2C
import time
i2c = I2C(I2C.I2C0,freq=100000, scl=0, sda=1)
time.sleep_ms(100)

MLX90614_IIC_ADDR	= const(0x5A)
MLX90614_TA			= const(0x06)
MLX90614_TOBJ1 		= const(0x07)
temp=0
class MLX90614:
  def __init__(self,i2c,addr=MLX90614_IIC_ADDR):
    self.addr=addr
    self.i2c=i2c

  def getObjCelsius(self):
        return self.getTemp(MLX90614_TOBJ1)	#Get celsius temperature of the object

  def getEnvCelsius(self):
        return self.getTemp(MLX90614_TA)	#Get celsius temperature of the ambient

  def getObjFahrenheit(self):
        return (self.getTemp(MLX90614_TOBJ1) * 9 / 5) + 32	#Get fahrenheit temperature of the object

  def getEnvFahrenheit(self):
        return (self.getTemp(MLX90614_TA) * 9 / 5) + 32	#Get fahrenheit temperature of the ambient


  def getTemp(self,reg):
        global temp
        temp = self.getReg(reg)*0.02-273.15	#Temperature conversion



  #def getReg(self,reg):
    #data = self.i2c.readfrom_mem(self.addr,reg,3) 							#Receive DATA
    #result = (data[1]<<8) | data[0]
    #return result
  def getReg(self,reg):
      try:
          data = self.i2c.readfrom_mem(self.addr,reg,3)
          result = (data[1]<<8) | data[0]#Receive DATA
          return result
      except:
          print("ads")
          result=0
          return result

ir = MLX90614(i2c)


while (1):
    ir.getObjCelsius()
    print("temp  %s *C"% (temp))
