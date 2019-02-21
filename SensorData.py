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
        #returns 4 bytes of data, LS 2bytes correspond to humidity and MS 2 bytes to temperature
 
	humid = output[0] + 256 * (output[1]) #converting raw form humidity sensor output in %
	hum_perc = (humid / 512) 	
	#print ("humidity is ",hum_perc , " / ", output )

	temp = output[2] + 256 * (output[3]) #converting raw form temperature sensor ouput to oC
	temperature = temp/512
	

	bus.write_i2c_block_data(0x5b,0x01,drivemode)
	bus.read_i2c_block_data(0x5b,0x01,1)
	output = bus.read_i2c_block_data(0x5b,0x02,4)
	#returns 4 bytes of data, LS 2 bytes correspond to C02 levels and MS 2 bytes correspond to TVOC
	eco2 = (output[0] << 8) | (output[1]) #Conversion of raw form data to C02 level in air in ppm (parts per million)
	tvoc = (output[2] << 8) | (output[3]) #Conversion of raw form data to Total Volatile Organic Compound level in ppm
	#print(" co2 level is = ", eco2)
	#print(" tvoc level is = ", tvoc)

	returnVal = {"humidity" : hum_perc,  "temperature": temperature, "CO2" : eco2, "VolatileComponents": tvoc}
	return returnVal
	#print (returnVal)
