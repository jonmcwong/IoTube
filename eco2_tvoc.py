import smbus
import time

bus=smbus.SMBus(1)

while True:
	emptylist=[]
	bus.write_i2c_block_data(0x5b,0xf4,emptylist)
	drivemode=[16]
	bus.write_i2c_block_data(0x5b,0x01,drivemode)
	bus.read_i2c_block_data(0x5b,0x01,1)
	output = bus.read_i2c_block_data(0x5b,0x02,4)
	eco2 = (output[0] << 8) | (output[1])
	tvoc = (output[2] << 8) | (output[3])
	print(" co2 level is = ", eco2)
	print(" tvoc level is = ", tvoc)
	time.sleep (10)

