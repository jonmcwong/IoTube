import smbus
import time
bus=smbus.SMBus(1)
while True:
	emptylist=[]
	bus.write_i2c_block_data(0x5b,0xf4,emptylist)
	drivemode=[32]
	bus.write_i2c_block_data(0x5b,0x05,drivemode)
	bus.read_i2c_block_data(0x5b,0x02,1)
	output = bus.read_i2c_block_data(0x5b,0x02,4)
	humidity = output[0] + 256 * (output[1])
	
	hum_perc = (humidity / 512) 	
	#temp = output [2:4]
	#parts = math.fmod(temperature)
	#fractional = parts[0]
	#temperature = parts[1]
	print ("humidity is ",hum_perc , " / ", output )
	time.sleep(30)