#TODO javascript mqqt comms

#program thatt runs on the raspberry pi.
#controls collecting data
#responds to data requests from the website
#stores collected data
import paho.mqtt.client as mqtt
import time
import json
from SensorData  import collect_data
import os
from pprint import pprint

#constants
ID = 243
SAMPLING_PERIOD = 1   #seconds
STATIONARY_PERIOD = 10  #seconds
MSG_POLL_PERIOD = 0.1 #seconds
#HOST = "ee-estott-octo.ee.ic.ac.uk"
HOST = "broker.hivemq.com"
PORT = 1883
#callbacks
def on_connect_cb(client, userdata, flags, rc):
  if rc != 0:
    print("Connection unsuccessful")
  else:
    print("Connection successful")
    #subscribing to specific topic to receive messages
    print("Subscribing...")
    device_topic = "IC.embedded/We.OG/" + str(ID)
    client.subscribe(topic=device_topic, qos=2)

def on_message_cb(client, userdata, message):  #message.payload is json
  print("Received message '" + str(message.payload) + "' on topic '" + message.topic + "' with QoS " + str(message.qos))
  #TODO
  print("got here 1")
  pprint(message.payload.decode())
  payload_json = json.loads(message.payload.decode())
  print("got here 4")
  time = payload_json['time']
  print("got here 3")
  #data = fetch_relevant_data(time) #returns dict
  data = collect_data()
  print("got here 2")
  #data = {}
  #data['test'] = "hello"
  print("got here 6")
  data.update(payload_json)
  print("got here 5")
  data = json.dumps(data)
  publish(data)
  print("got to end of on_message")

def on_publish_cb(client, userdata, mid):
  print("Published")
  
def on_disconnect_cb(client, userdata, rc):
  if rc != 0:
    print("Unexpected disconnection.")
    setup_mqtt()
  else:
    print("Disconnected successfully!")

def on_subscribe_cb(client, userdata, mid, granted_qos):
  print("Subscibed, will start receiving messages") 
#-------------------------------------------------------------------


def wait_for_response(client, flag):
  start_time = time.time()
  while not flag:
    print("flag is " + str(flag))
    client.loop()                      #waits for result, blocking
  print("Completed in " + str(time.time() - start_time) + " seconds")

def setup_mqtt(client, ID):
  client.on_connect = on_connect_cb
  client.on_message = on_message_cb
  client.on_publish = on_publish_cb
  client.on_disconnect = on_disconnect_cb  #this call back causes errors
  client.on_subscribe = on_subscribe_cb

  #connecting to client
  print("Trying to connect...")
  #client.tls_set(ca_certs="mosquitto.org.crt", certfile="client.crt",keyfile="client.key")
  client.connect(host=HOST,port=PORT)
    #client.connect(host="test.mosquitto.org",port=1883)

def publish(json_str):  #sending message to broker
  #json_str must be stringified
  print("Publishing \"" + json.dumps(json_str) + "\"...")
  device_topic = "IC.embedded/We.OG/return"
  print("got to publish")
  MSG_INFO = client.publish(topic=device_topic, payload=json_str, qos=2)
  mqtt.error_string(MSG_INFO.rc)
#----------------------------------------------------------------------
#request responses

def fetch_relevant_data(time):
  #TODO
  #start = next( (x for x in reverse(log) if x['time']<time), default_value)
  #stop =
  return
#-------------------------------------------------------------------

#main
client = mqtt.Client()
client.connected_flag = False
client.subscribed_flag = False
setup_mqtt(client, ID)
with open('data.txt', 'w+') as json_file:
  if os.stat("data.txt").st_size == 0:
    log = []
  else:
    try:
      log = json.load(json_file)
    except ValueError:
      log = []
sample_timer = time.time()
loop_timer = time.time()
while True: #all of this is BS unless the functions are defined in later code
  #timing of data sampling
  #keeps all data until file is emptied
  #TODOlogic for data sending must be decided
  if time.time() > sample_timer + SAMPLING_PERIOD:
    data = collect_data() #should be json
    data["time"] = time.localtime( time.time())
    log.append(data)
    with open('data.txt', 'w') as outfile:
      json.dump(log, outfile)
    sample_timer = time.time()
  #timing of network checking
  if time.time() > loop_timer + MSG_POLL_PERIOD:
    client.loop()
