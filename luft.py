#!/usr/bin/env python3
import time
import board
import adafruit_dht
import paho.mqtt.client as mqtt

dht_device = adafruit_dht.DHT22(board.D4)

mqttc = mqtt.Client()
mqttc.connect("10.10.10.8")

h_id = "air01"
h_name = "Air 01"

tb = f"homie/{h_id}"
tbd = f"{tb}/dht22"

def publish_retained(topic, payload):
    mqttc.publish(f"{tb}/{topic}", payload=payload)

publish_retained("$state", "init")

publish_retained("$homie", "3.0.1")

mqttc.loop()

publish_retained("$name", h_name)
publish_retained("$nodes", "dht22")
publish_retained("$stats", "uptime")
mqttc.loop()

publish_retained("dht22/$name", "DHT22 Sensor")
publish_retained("dht22/$type", "Senseless Homie Type")
publish_retained("dht22/$properties", "temperature,humidity")
mqttc.loop()

publish_retained("dht22/temperature/$name", "Lufttemperatur")
publish_retained("dht22/temperature/$datatype", "float")
publish_retained("dht22/temperature/$unit", "ºC")
mqttc.loop()

publish_retained("dht22/humidity/$name", "Luftfeuchtigkeit")
publish_retained("dht22/humidity/$datatype", "float")
publish_retained("dht22/humidity/$unit", "%")
mqttc.loop()

publish_retained("$state", "ready")
mqttc.loop()

uptime = 0
sleep_seconds = 5

def send_stats():
    publish_retained("$stats/uptime", f"{uptime}")

while True:
    mqttc.loop()

    if uptime % 30 == 0:
        send_stats()

    uptime += sleep_seconds
    time.sleep(sleep_seconds)

    try:
        temperature_c = dht_device.temperature
        humidity = dht_device.humidity
        print("Temp={0:0.1f}ºC  Humidity={1:0.1f}%".format(temperature_c, humidity))
        publish_retained("dht22/temperature", f"{temperature_c}")
        publish_retained("dht22/humidity", f"{humidity}")
    except RuntimeError as error:
        print(error.args[0])
    except Exception as error:
        dht_device.exit()
        raise error

