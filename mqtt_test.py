print ("Test begin")
import paho.mqtt.client as mqtt
print ("\n \n \n Mqtt")
client = mqtt.Client()
print ("\n \n \n Client")
client.tls_set(ca_certs="mosquitto.org.crt", certfile="client.crt",keyfile="client.key")
print ("\n \n \n Certificate")
client.connect ("test.mosquitto.org" ,port=8884)
print ("\n \n \n Connected")
MSG_INFO = client.publish("IC.embedded/We.OG","hello")
mqtt.error_string(MSG_INFO.rc)
def on_message(client, userdata, message) :
	print("on message")
	print("Received message:{} on topic{}".format(message.payload, message.topic))
client.on_message = on_message
client.subscribe("IC.embedded/We.OG/")
print("subscribed")
client.loop()
print("loop")
