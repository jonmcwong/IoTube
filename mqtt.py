#Demonstrates connecting to the broker using encryption, 
#subscribing to a topic, asynchronously handling incoming 
#messages and publishing



import paho.mqtt.client as mqtt
import time

client = mqtt.Client()

def wait_for_response():
  start_time = time.time()
  client.loop(0.1)                      #waits for result, blocking
  if time.time() - start_time > 60:
    print("\tError, Timed out")
  else:
    print("\tCompleted in {} seconds" .format(time.time() - start_time))

def setup_mqtt():
  #connecting to client
  print("Trying to connect...")
  client.tls_set(ca_certs="mosquitto.org.crt", certfile="client.crt",keyfile="client.key")
  client.connect(host="test.mosquitto.org",port=8884)
  #client.connect(host="test.mosquitto.org",port=1883)
  wait_for_response()

  #subscribing to specific topic to receive messages
  print("Subscribing...")
  client.subscribe(topic="IC.embedded/We.OG", qos=2)
  wait_for_response()
  print("Type text to publish")


def publish(msg):
  #sending message to broker
  print("Publishing \"" + msg + "\"...")
  MSG_INFO = client.publish(topic="IC.embedded/We.OG", payload=msg, qos=2)
  mqtt.error_string(MSG_INFO.rc)

#setup client and define callbacks
def on_connect_cb(client, userdata, flags, rc):
  if rc != 0:
    print("Connection unsuccessful")
  else:
    print("Connection successful")

def on_message_cb(client, userdata, message):
  print("Received message '" + str(message.payload) + "' on topic '"
    + message.topic + "' with QoS " + str(message.qos))

def on_publish_cb(client, userdata, mid):
  print("Published")
  
def on_disconnect_cb(client, userdata, rc):
  if rc != 0:
    print("Unexpected disconnection.")
    setup_mqtt()
  else:
    print("Disconnected successfully!")

def on_subscribe_cb(client, userdata, mid, granted_qos):
  print("Subscibed")

#client.on_connect = on_connect_cb
client.on_message = on_message_cb
client.on_publish = on_publish_cb
#client.on_disconnect = on_disconnect_cb  #this call back causes errors
#client.on_subscribe = on_subscribe_cb

#start mqtt
setup_mqtt()
client.loop_start() #start expecting messages
while True:
  msg = input()
  publish(msg)
