#This code reads the data from the ToF sensor
#An offset is taken off
#Date and time is used to package reading as a 
#key/value pair stored as a Json in sensorStr 
import board
import busio
import adafruit_vl6180x
import datetime
import time
import json

def getRange():
  OFFSET = 19
  i2c = busio.I2C(board.SCL, board.SDA)
  sensor = adafruit_vl6180x.VL6180X(i2c)
  measurement = sensor.range - OFFSET
  currentDate = datetime.datetime.now()
  ##print('{0}mm'.format(measurement))
  sensorStr = json.dumps({currentDate.strftime("%Y-%m-%d %H:%M:%S") : measurement})
  #print(sensorStr)
  return sensorStr
  
