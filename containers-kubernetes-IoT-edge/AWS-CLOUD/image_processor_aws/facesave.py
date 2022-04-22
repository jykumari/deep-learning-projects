import sys
import paho.mqtt.client as mqtt

LOCAL_MQTT_HOST="mosquitto"
LOCAL_MQTT_PORT=1883
LOCAL_MQTT_TOPIC="face_save"
S3_MOUNT = "/mnt/mountpoint/facehw3/"
QOS = 0
count = 0

# create mqtt on_connect callback
def on_connect_local(client, userdata, flags, rc):
    print("connected to local broker with rc: " + str(rc))
    client.subscribe(LOCAL_MQTT_TOPIC, QOS)

# create mqtt on_subscribe callback
def on_subscribe_local(client, userdata, msgid, qos):
    print("Subscribed to Topic",LOCAL_MQTT_TOPIC, "with Granted QOS", qos)
    print("Waiting for Messages...\n")

# create mqtt on_message callback
def on_message(client, userdata, msg):
  try:
    global count
    count +=1
    print("Message Received with QOS", msg.qos, "on Topic:", msg.topic, "count: ", count)
    
    # create file name
    fileName = "image"+str(count)+'.png'

    # save image to s3 mounted drive
    path = S3_MOUNT+fileName
    imgFile = open(path, 'wb')
    imgFile.write(msg.payload)
    imgFile.close()
    print("Image saved to", S3_MOUNT, "as", fileName+"\n")
  except:
    print("Unexpected error:", sys.exc_info()[0])


# create mqtt client; initiate callback functions; connect to cloud host
local_mqttclient = mqtt.Client()
local_mqttclient.on_connect = on_connect_local
local_mqttclient.on_subscribe = on_subscribe_local
local_mqttclient.on_message = on_message
local_mqttclient.connect(LOCAL_MQTT_HOST, LOCAL_MQTT_PORT, 60)


# go into a loop
local_mqttclient.loop_forever()

