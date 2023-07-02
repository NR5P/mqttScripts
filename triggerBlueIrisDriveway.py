import paho.mqtt.client as mqtt

# MQTT broker configuration
BROKER_ADDRESS = "10.74.92.143"
TOPIC_SUBSCRIBE = "/gate/carAlertPressureSensor"
TOPIC_PUBLISH = "BlueIris/admin"

# Define the MQTT message handler
def on_message(client, userdata, message):
    print("Received message:", message.payload.decode())
    if message.payload.decode() == "ALERT":
        # Publish a message to the BlueIris/admin topic
        client.publish(TOPIC_PUBLISH, "camera=gateCamera&trigger")

# Connect to the MQTT broker
client = mqtt.Client()
client.on_message = on_message
client.connect(BROKER_ADDRESS)

# Subscribe to the topic
client.subscribe(TOPIC_SUBSCRIBE)

# Start the MQTT message loop
client.loop_forever()
