import paho.mqtt.client as mqtt
from ipPhone import make_call

# MQTT broker configuration
BROKER_ADDRESS = "192.168.1.246"
TOPIC_SUBSCRIBE = "/gate/carAlertPressureSensor"
TOPIC_PUBLISH = "BlueIris/admin"

# Define the MQTT message handler
def on_message(client, userdata, message):
    print("Received message:", message.payload.decode())
    if message.payload.decode() == "ALERT":
        # Publish a message to the BlueIris/admin topic
        client.publish(TOPIC_PUBLISH, "camera=gateCamera&trigger")
        make_call("192.168.1.22") #make a call to home ip phone
        make_call("192.168.1.21") #make a call to office ip phone

# Connect to the MQTT broker
client = mqtt.Client()
client.on_message = on_message
client.connect(BROKER_ADDRESS)

# Subscribe to the topic
client.subscribe(TOPIC_SUBSCRIBE)

# Start the MQTT message loop
client.loop_forever()
