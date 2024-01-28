import machine
from machine import Pin
from machine import freq
import time
import network
from umqtt.simple import MQTTClient
from hx711 import HX711

# micropython hx711 library
#https://github.com/SergeyPiskunov/micropython-hx711

TRIGGER_WEIGHT = 2000

freq(160000000)
driver = HX711(d_out=5, pd_sck=4)

# WiFi settings
WIFI_SSID = ""
WIFI_PASSWORD = ""

# MQTT settings
MQTT_BROKER = "10.74.92.143"
MQTT_PORT = 1883
MQTT_TOPIC = "/gate/carAlertPressureSensor"
MQTT_CLIENT_ID = "carAlertPressureSensor"

# Pin for the event
event_pin = Pin(15, Pin.IN)

# Connect to WiFi
wifi = network.WLAN(network.STA_IF)
wifi.active(True)

# Connect to MQTT broker
mqtt_client = MQTTClient(MQTT_CLIENT_ID, MQTT_BROKER, MQTT_PORT)

def connect_to_mqtt():
    mqtt_client.connect()
    print("Connected to MQTT broker")

# Function to handle the event
def handle_event():
    message = "ALERT"
    mqtt_client.publish(MQTT_TOPIC, message)
    print("Published message:", message)

def connect_to_wifi():
    wifi.connect(WIFI_SSID, WIFI_PASSWORD)
    while not wifi.isconnected():
        pass
    print("Connected to Wi-Fi")

def handle_reconnection():
    while not wifi.isconnected():
        connect_to_wifi()
        time.sleep(1)
    while not mqtt_client.is_connected():
        print("MQTT connection lost. Reconnecting...")
        connect_to_mqtt()
        time.sleep(1)

def checkWeightTrigger():
    weight = driver.read()/1000
    #print(weight) testing only
    if weight > TRIGGER_WEIGHT:
        print("triggered")
        return True
    return False

# Configure interrupt for the event pin
#event_pin.irq(trigger=Pin.IRQ_RISING, handler=handle_event)

# Main loop
while True:
    if wifi.isconnected():
        try:
            if checkWeightTrigger():
                handle_event()
        except OSError:
            print("MQTT connection lost. Reconnecting...")
            handle_reconnection()
    else:
        print("Wi-Fi connection lost. Reconnecting...")
        handle_reconnection()