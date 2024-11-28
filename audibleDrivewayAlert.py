import network
import time
from machine import Pin
from umqtt.simple import MQTTClient

# WiFi settings
WIFI_SSID = "bugsquashed"
WIFI_PASSWORD = "cooltomato001"

# MQTT settings
MQTT_BROKER = "10.74.92.143"
MQTT_PORT = 1883
MQTT_TOPIC = "/gate/carAlertPressureSensor"
MQTT_CLIENT_ID = "audibleDrivewayAlert"

chime_frequency = 1000  # Adjust this value to change the pitch of the chime
chime_duration = 0.2   # Adjust this value to change the length of the chime sound

# Pin for performing the action
action_pin = Pin(15, Pin.OUT)
buzzer_pin = Pin(12, Pin.OUT)

# Connect to Wi-Fi
wifi = network.WLAN(network.STA_IF)
wifi.active(True)
wifi.connect(WIFI_SSID, WIFI_PASSWORD)
while not wifi.isconnected():
    pass
print("Connected to WiFi")

# MQTT message callback
def mqtt_callback(topic, msg):
    if topic == MQTT_TOPIC and msg == b"ALERT":
        perform_action()

# Perform the action
def perform_action():
    print("Performing action...")
    # Example action: Toggle the state of the action pin
    action_pin.value(not action_pin.value())
    play_chime()
    time.sleep(1)

def play_chime():
    pwm = PWM(buzzer_pin)
    pwm.freq(chime_frequency)
    pwm.duty(512)  # Adjust this value to change the volume of the chime
    time.sleep(chime_duration)
    pwm.deinit()

# Connect to MQTT broker and subscribe to the topic
mqtt_client = MQTTClient(MQTT_CLIENT_ID, MQTT_BROKER, MQTT_PORT)
mqtt_client.set_callback(mqtt_callback)
mqtt_client.connect()
mqtt_client.subscribe(MQTT_TOPIC)
print("Connected to MQTT broker and subscribed to topic:", MQTT_TOPIC)

# Main loop
while True:
    mqtt_client.check_msg()  # Check for new MQTT messages
    # Your main program logic here
    time.sleep(1)