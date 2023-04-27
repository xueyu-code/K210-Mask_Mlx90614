
#=======================测温外加口罩识别=====================#
from machine import I2C
import time
import sensor, image, lcd, time
import KPU as kpu
i2c = I2C(I2C.I2C0,freq=100000, scl=0, sda=1)
time.sleep_ms(100)

color_R = (255, 0, 0)
color_G = (0, 255, 0)
color_B = (0, 0, 255)

MLX90614_IIC_ADDR	= const(0x5A)
MLX90614_TA			= const(0x06)
MLX90614_TOBJ1 		= const(0x07)

temp=0
data=0
def drawConfidenceText(image, rol, classid, value):
    text = ""
    _confidence = int(value * 100)

    if classid == 1:
        text = 'mask: ' + str(_confidence) + '%'
        color_text=color_G
    else:
        text = 'no_mask: ' + str(_confidence) + '%'
        color_text=color_R
    image.draw_string(rol[0], rol[1], text, color=color_text, scale=2.5)

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
        data=temp

  def getReg(self,reg):#用try处理抛出的异常
      try:
          data = self.i2c.readfrom_mem(self.addr,reg,3)
          result = (data[1]<<8) | data[0]#Receive DATA
          return result
      except:
          print("ads")
          result=0
          return result

ir = MLX90614(i2c)
lcd.init()
sensor.reset(dual_buff=True)
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.QVGA)
sensor.set_hmirror(0)
sensor.run(1)


task = kpu.load(0x300000)


anchor = (0.1606, 0.3562, 0.4712, 0.9568, 0.9877, 1.9108, 1.8761, 3.5310, 3.4423, 5.6823)
_ = kpu.init_yolo2(task, 0.5, 0.3, 5, anchor)
img_lcd = image.Image()


while (True):
    ir.getObjCelsius()
    img = sensor.snapshot()
    code = kpu.run_yolo2(task, img)
    if code:
        totalRes = len(code)

        for item in code:
            confidence = float(item.value())
            itemROL = item.rect()
            classID = int(item.classid())

            if confidence < 0.52:
                _ = img.draw_rectangle(itemROL, color=color_B, tickness=5)
                continue

            if classID == 1 and confidence > 0.65:
                _ = img.draw_rectangle(itemROL, color_G, tickness=5)
                if totalRes == 1:
                    drawConfidenceText(img, (0, 0), 1, confidence)
            else:
                _ = img.draw_rectangle(itemROL, color=color_R, tickness=5)
                if totalRes == 1:
                    drawConfidenceText(img, (0, 0), 0, confidence)
    img.draw_string(0,200, ("%s" %(temp)), color=(0,0,255), scale=2)
    _ = lcd.display(img)
    #lcd.draw_string(100, 100,data, lcd.RED, lcd.BLACK)
