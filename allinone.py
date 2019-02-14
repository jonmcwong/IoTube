import smbus
import time
import math
from decimal import Decimal

bus=smbus.SMBus(1)
while True:
	emptylist=[]
	bus.write_i2c_block_data(0x5b,0xf4,emptylist)
	drivemode=[16]

	bus.write_i2c_block_data(0x5b,0x05,drivemode)
	bus.read_i2c_block_data(0x5b,0x02,1)
	output = bus.read_i2c_block_data(0x5b,0x02,4)
	humidity = output[0] + 256 * (output[1])
	hum_perc = (humidity / 512) 	
	print ("humidity is ",hum_perc , " / ", output )
	
	bus.write_i2c_block_data(0x5b,0x05,drivemode)
	bus.read_i2c_block_data(0x5b,0x02,1)
	output = bus.read_i2c_block_data(0x5b,0x02,4)
	
	#vref = ( output[0] << 8 )| output[1]
	#vrntc = (output[2] << 8) | output[3]
	#rntc = (float(vrntc) * float (100000)/ float(vref) )

	#ntc_temp = Decimal(math.log(rntc / 10000))
	#print(" ", ntc_temp)
	#ntc_temp = Decimal (ntc_temp / 3380)
	#print(" ", ntc_temp)
	#ntc_temp = Decimal(ntc_temp + Decimal(1 / (25 + 273.15)))
	#print(" ", ntc_temp)
	#ntc_temp = Decimal((Decimal(1))/ntc_temp)
	#print(" ", ntc_temp)
	#ntc_temp = Decimal(ntc_temp - Decimal(298.15))
	#print ("temp is", ntc_temp," ", rntc )

	time.sleep(10)

	bus.write_i2c_block_data(0x5b,0x01,drivemode)
	bus.read_i2c_block_data(0x5b,0x01,1)
	output = bus.read_i2c_block_data(0x5b,0x02,4)
	eco2 = (output[0] << 8) | (output[1])
	tvoc = (output[2] << 8) | (output[3])
	print(" co2 level is = ", eco2)
	print(" tvoc level is = ", tvoc)

	time.sleep(10)