import time
from getRange import getRange


PERIOD = 10.0
count = PERIOD
startTime = time.time()
while True:
  if count == 0:
    count = PERIOD
    print("fps: ", 1.0*PERIOD/(time.time()-startTime))
    startTime = time.time()
  getRange()
  count -=  1
  
