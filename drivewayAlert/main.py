import network
import time
from machine import Pin, PWM
from umqtt.simple import MQTTClient

# WiFi settings
WIFI_SSID = ""
WIFI_PASSWORD = ""

# Define the frequency values for the notes
NOTE_C4 = 261
NOTE_DFLAT4 = 277
NOTE_D4 = 293
NOTE_EFLAT4 = 311
NOTE_E4 = 329
NOTE_F4 = 349
NOTE_GFLAT4 = 369
NOTE_G4 = 391
NOTE_AFLAT4 = 415
NOTE_A4 = 440
NOTE_BFLAT4 = 466
NOTE_B4 = 493
NOTE_C5 = 523
NOTE_DFLAT5 = 554
NOTE_D5 = 587
NOTE_EFLAT5 = 622
NOTE_E5 = 659
NOTE_F5 = 698
NOTE_GFLAT5 = 739
NOTE_G5 = 783
NOTE_AFLAT5 = 830
NOTE_A5 = 880
NOTE_BFLAT5 = 932
NOTE_B5 = 987
NOTE_C6 = 1046


# Define the durations for the notes (in milliseconds)
SIXTEENTH_NOTE = 100
EIGHTH_NOTE = 2 * SIXTEENTH_NOTE
QUARTER_NOTE = 2 * EIGHTH_NOTE
HALF_NOTE = 2 * QUARTER_NOTE

# Define the melody for the beginning of "P.I.M.P."
"""
melody = [
    (NOTE_AFLAT5, SIXTEENTH_NOTE), 
    (NOTE_GFLAT5, SIXTEENTH_NOTE), 
    (NOTE_EFLAT5, SIXTEENTH_NOTE), 
    (NOTE_BFLAT5, SIXTEENTH_NOTE), 
    (NOTE_AFLAT5, SIXTEENTH_NOTE), 
    (NOTE_GFLAT5, EIGHTH_NOTE), 
    (NOTE_EFLAT5, EIGHTH_NOTE), 
    (NOTE_DFLAT5, EIGHTH_NOTE), 
    (NOTE_EFLAT5, EIGHTH_NOTE), 
    (NOTE_EFLAT5, QUARTER_NOTE), 
    (None, QUARTER_NOTE),
    (NOTE_EFLAT5, SIXTEENTH_NOTE), 
    (NOTE_EFLAT5, SIXTEENTH_NOTE), 
    (NOTE_EFLAT5, SIXTEENTH_NOTE), 
    (NOTE_G5, SIXTEENTH_NOTE), 
    (NOTE_G5, EIGHTH_NOTE), 
    (NOTE_G5, SIXTEENTH_NOTE), 
    (NOTE_G5, SIXTEENTH_NOTE), 
    (NOTE_G5, SIXTEENTH_NOTE), 
    (NOTE_EFLAT5, EIGHTH_NOTE), 
    (NOTE_BFLAT5, EIGHTH_NOTE), 
    (None, QUARTER_NOTE),
    (NOTE_EFLAT5, SIXTEENTH_NOTE), 
    (NOTE_EFLAT5, SIXTEENTH_NOTE), 
    (NOTE_EFLAT5, SIXTEENTH_NOTE), 
    (NOTE_GFLAT5, SIXTEENTH_NOTE), 
    (NOTE_GFLAT5, SIXTEENTH_NOTE), 
    (NOTE_GFLAT5, SIXTEENTH_NOTE), 
    (NOTE_GFLAT5, SIXTEENTH_NOTE), 
    (NOTE_GFLAT5, SIXTEENTH_NOTE), 
    (NOTE_F5, SIXTEENTH_NOTE), 
    (None, QUARTER_NOTE),
    (NOTE_EFLAT5, SIXTEENTH_NOTE), 
    (NOTE_EFLAT5, SIXTEENTH_NOTE), 
    (NOTE_F5, EIGHTH_NOTE), 
    (NOTE_F5, SIXTEENTH_NOTE), 
    (NOTE_F5, SIXTEENTH_NOTE), 
    (NOTE_F5, SIXTEENTH_NOTE), 
    (NOTE_A5, SIXTEENTH_NOTE), 
    (NOTE_A5, EIGHTH_NOTE), 
    (NOTE_A5, SIXTEENTH_NOTE), 
    (NOTE_A5, SIXTEENTH_NOTE), 
    (NOTE_A5, SIXTEENTH_NOTE), 
    (NOTE_F5, EIGHTH_NOTE), 
    (NOTE_BFLAT5, SIXTEENTH_NOTE), 
    (None, QUARTER_NOTE)
]
"""

melody = [
    (NOTE_AFLAT5, SIXTEENTH_NOTE), 
    (NOTE_GFLAT5, SIXTEENTH_NOTE), 
    (NOTE_EFLAT5, SIXTEENTH_NOTE), 
    (NOTE_BFLAT5, SIXTEENTH_NOTE), 
    (NOTE_AFLAT5, SIXTEENTH_NOTE), 
    (NOTE_GFLAT5, EIGHTH_NOTE), 
    (NOTE_EFLAT5, EIGHTH_NOTE), 
    (NOTE_DFLAT5, EIGHTH_NOTE), 
    (NOTE_EFLAT5, EIGHTH_NOTE), 
    (NOTE_EFLAT5, QUARTER_NOTE), 
]




# MQTT settings
MQTT_BROKER = "10.74.92.143"
MQTT_PORT = 1883
MQTT_TOPIC = "/gate/carAlertPressureSensor"
MQTT_CLIENT_ID = "audibleDrivewayAlert"

chime_frequency = 1000  # Adjust this value to change the pitch of the chime
chime_duration = 1.0   # Adjust this value to change the length of the chime sound
duty_cycle = 400

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
    if topic.decode("utf-8") == MQTT_TOPIC and msg.decode("utf-8") == "ALERT":
        perform_action()

# Perform the action
def perform_action():
    print("Performing action...")
    # Example action: Toggle the state of the action pin
    action_pin.value(not action_pin.value())
    play_chime_pimp()
    time.sleep(1)

def play_chime_pimp():
    pwm = PWM(buzzer_pin)
    # Play the melody
    for note, duration in melody:
        if note is None:  # Pause (rest)
            time.sleep_ms(duration)
        else:
            frequency, duration = (note, duration)
            pwm.freq(frequency)
            pwm.duty(50)  # Adjust the duty cycle if necessary
            time.sleep_ms(duration)
            pwm.duty(0)
    pwm.deinit()


def play_chime():
    pwm = PWM(buzzer_pin)
    pwm.freq(chime_frequency)
    pwm.duty(duty_cycle)  # Adjust this value to change the volume of the chime
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
    #perform_action()
    mqtt_client.check_msg()  # Check for new MQTT messages
    time.sleep(1)