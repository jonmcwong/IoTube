import smbus

from Adafruit_CCS811 import Adafruit_CCS811

def collect_data():
	bus=smbus.SMBus(1)
	emptylist=[]
	bus.write_i2c_block_data(0x5b,0xf4,emptylist)
	drivemode=[16]

	bus.write_i2c_block_data(0x5b,0x05,drivemode)
	bus.read_i2c_block_data(0x5b,0x02,1)
	output = bus.read_i2c_block_data(0x5b,0x02,4)
	humid = output[0] + 256 * (output[1])
	hum_perc = (humid / 512) 	
	humidityVal = {"humidity" : hum_perc}
	#print ("humidity is ",hum_perc , " / ", output )

	tempVal = {"temperature": '20'}

	bus.write_i2c_block_data(0x5b,0x01,drivemode)
	bus.read_i2c_block_data(0x5b,0x01,1)
	output = bus.read_i2c_block_data(0x5b,0x02,4)
	eco2 = (output[0] << 8) | (output[1])
	tvoc = (output[2] << 8) | (output[3])
	co2Val = {"CO2" : eco2}
	tvocVal = {"Volatile Components": tvoc}
	#print(" co2 level is = ", eco2)
	#print(" tvoc level is = ", tvoc)

	returnVal = {"humidity" : hum_perc,  "temperature": 20, "CO2" : eco2, "VolatileComponents": tvoc}
	return returnVal
	#print (returnVal)
