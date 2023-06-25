import machine
from machine import Pin
from machine import freq
import time
import network
from umqtt.simple import MQTTClient
from hx711 import HX711

# micropython hx711 library
#https://github.com/SergeyPiskunov/micropython-hx711

TRIGGER_WEIGHT = 10000

freq(160000000)
driver = HX711(d_out=5, pd_sck=4)

# WiFi settings
WIFI_SSID = "your_wifi_ssid"
WIFI_PASSWORD = "your_wifi_password"

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
wifi.connect(WIFI_SSID, WIFI_PASSWORD)
while not wifi.isconnected():
    pass
print("Connected to WiFi")

# Connect to MQTT broker
mqtt_client = MQTTClient(MQTT_CLIENT_ID, MQTT_BROKER, MQTT_PORT)
mqtt_client.connect()
print("Connected to MQTT broker")

# Function to handle the event
def handle_event():
    message = "Event occurred!"
    mqtt_client.publish(MQTT_TOPIC, message)
    print("Published message:", message)

def checkWeightTrigger():
    if driver.read() > TRIGGER_WEIGHT:
        return True
    return False

# Configure interrupt for the event pin
#event_pin.irq(trigger=Pin.IRQ_RISING, handler=handle_event)

# Main loop
while True:
    # Your main program logic here
    time.sleep_ms(250)
    if checkWeightTrigger():
        handle_event()
