import paho.mqtt.client as mqtt
import sys

LOCAL_MQTT_HOST="package-broker-service"
LOCAL_MQTT_PORT=1883
LOCAL_MQTT_TOPIC="object_sent"

count = 0
def on_connect_local(client, userdata, flags, rc):
    print("connected to local broker with rc: " + str(rc))
    client.subscribe(LOCAL_MQTT_TOPIC)
	
def on_message(client,userdata, msg):
  try:
    global count
    count += 1
    print("message "+ str(count) + " received:  detected " + str(msg.payload.decode("utf-8")))
    
  except:
    print("Unexpected error:", sys.exc_info()[0])

local_mqttclient = mqtt.Client()
local_mqttclient.on_connect = on_connect_local
local_mqttclient.connect(LOCAL_MQTT_HOST, LOCAL_MQTT_PORT, 60)
local_mqttclient.on_message = on_message



# go into a loop
local_mqttclient.loop_forever()
