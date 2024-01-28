import machine
from machine import Pin
from machine import freq
import time
import network
from umqtt.simple import MQTTClient
from hx711 import HX711

# micropython hx711 library
#https://github.com/SergeyPiskunov/micropython-hx711

TRIGGER_WEIGHT = 100

freq(160000000)
driver = HX711(d_out=5, pd_sck=4)

# WiFi settings
WIFI_SSID = ""
WIFI_PASSWORD = ""

# MQTT settings
MQTT_BROKER = "192.168.1.246"
MQTT_PORT = 1883
MQTT_TOPIC = "/gate/carAlertPressureSensor"
GATE_OPENER_TOPIC = "/gate/command/openClose"
MQTT_CLIENT_ID = "carAlertPressureSensor"

queue = []
triggered = False

#gate opener
gateOpenerPin = Pin(23,Pin.OUT)
gateOpenerPin.value(0)

# Pin for the event
event_pin = Pin(15, Pin.IN)

# Connect to WiFi
wifi = network.WLAN(network.STA_IF)
wifi.active(True)

# Connect to MQTT broker
mqtt_client = MQTTClient(MQTT_CLIENT_ID, MQTT_BROKER, MQTT_PORT)

def on_message(topic, msg):
    if msg == b"TOGGLE":
        print("opening gate")
        gateOpenerPin.value(1)
        time.sleep(1)
        gateOpenerPin.value(0)


def connect_to_mqtt():
    mqtt_client.set_callback(on_message)
    mqtt_client.connect()
    mqtt_client.subscribe(GATE_OPENER_TOPIC)
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
    time.sleep(5)
    wifi.active(False)
    wifi.active(True)
    while not wifi.isconnected():
        connect_to_wifi()
        time.sleep(1)
    connect_to_mqtt()

def checkWeightTrigger():
    triggered = False
    weight = driver.read()/1000
    queue.append(weight)
    if len(queue) > 4:
        queue.pop(0)
        if (queue[3] - queue[1]) > TRIGGER_WEIGHT and (queue[2] - queue[0]) > TRIGGER_WEIGHT:
            triggered = True
    if triggered:
        print("driveway sensor triggered")
        return True
    return False

# Configure interrupt for the event pin
#event_pin.irq(trigger=Pin.IRQ_RISING, handler=handle_event)

# Main loop
while True:
    if wifi.isconnected():
        try:
            mqtt_client.check_msg()
            if checkWeightTrigger():
                handle_event()
                time.sleep(10)
        except OSError:
            print("MQTT connection lost. Reconnecting...")
            handle_reconnection()
    else:
        print("Wi-Fi connection lost. Reconnecting...")
        handle_reconnection()