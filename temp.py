import smbus
import time
import math
from decimal import Decimal
import csv

bus=smbus.SMBus(1)
while True:
	emptylist=[]
	bus.write_i2c_block_data(0x5b,0xf4,emptylist)
	drivemode=[32]
	bus.write_i2c_block_data(0x5b,0x05,drivemode)
	bus.read_i2c_block_data(0x5b,0x02,1)
	output = bus.read_i2c_block_data(0x5b,0x02,4)
	
	vref = ( output[0] << 8 )| output[1]
	vrntc = (output[2] << 8) | output[3]
	rntc = (float(vrntc) * float (100000)/ float(vref) )

	ntc_temp = Decimal(math.log(rntc / 10000))
	print(" ", ntc_temp)
	ntc_temp = Decimal (ntc_temp / 3380)
	print(" ", ntc_temp)
	ntc_temp = Decimal(ntc_temp + Decimal(1 / (25 + 273.15)))
	print(" ", ntc_temp)
	ntc_temp = Decimal((Decimal(1))/ntc_temp)
	print(" ", ntc_temp)
	ntc_temp = Decimal(ntc_temp - Decimal(311.15))
	#data = []
	#with open ('temp.csv' ) as f:
	#	reader = csv.reader(f)
	#with open ('temp.csv' , 'w') as csvFile:
	#	writer = csv.writer(csvFile)
	#	data.append(ntc_temp)
	#	writer.writerows(data)
	print ("temp is", ntc_temp," ", output )
	time.sleep(1)