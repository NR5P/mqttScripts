#!/usr/bin/python3


import time
import datetime
import paho.mqtt.client as mqtt

# MQTT broker details
broker = "10.74.92.143"
port = 1883
topic = "is_night"

# MQTT client setup
client = mqtt.Client()

def on_connect(client, userdata, flags, rc):
    print("Connected to MQTT broker")
    client.subscribe(topic)

def on_publish(client, userdata, mid):
    print("is night published")

def on_disconnect(client, userdata, rc):
    print("Disconnected from MQTT broker")

client.on_connect = on_connect
client.on_publish = on_publish
client.on_disconnect = on_disconnect

# Connect to MQTT broker
client.connect(broker, port, 60)

while True:
    try:
        # Get current time
        #current_time = datetime.datetime.now().strftime("%H:%M:%S")
        current_time = datetime.datetime.now().time()

        # Check if time is after 8 PM and before 6 AM
        is_in_range = current_time > datetime.time(20, 0) or current_time < datetime.time(6, 0)

        # Publish time to MQTT broker
        client.publish(topic, str(is_in_range))

        # Wait for 1 second before publishing again
        time.sleep(5)
    except KeyboardInterrupt:
        break

# Disconnect from MQTT broker
client.disconnect()
