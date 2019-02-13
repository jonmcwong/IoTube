import smbus
import time
import math
bus=smbus.SMBus(1)
while True:
	emptylist=[]
	bus.write_i2c_block_data(0x5b,0xf4,emptylist)
	drivemode=[16]
	bus.write_i2c_block_data(0x5b,0x05,drivemode)
	bus.read_i2c_block_data(0x5b,0x02,1)
	output = bus.read_i2c_block_data(0x5b,0x02,4)
	
	vref = ( output[0] << 8 )| output[1]
	vrntc = (output[2] << 8) | output[3]
	rntc = (float(vrntc) * float (100000)/ float(vref) )

	ntc_temp = math.log(rntc / 10000.0)
	ntc_temp /= 3380.0
	ntc_temp += 1.0 / (25 + 273.15)
	ntc_temp = 1.0 / ntc_temp
	ntc_temp -= 273.15
	print ("temp is", ntc_temp -25.0," ", output )
	time.sleep(30)