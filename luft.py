#!/usr/bin/env python3
import time
import board
import adafruit_dht
import homie

dht_device = adafruit_dht.DHT22(board.D4)

Homie = homie.Homie(homie.loadConfigFile("homie.json"))
h_temperature_node = Homie.Node("temperature", "temperature")
h_humidity_node = Homie.Node("humidity", "humidity")
Homie.setFirmware("awesome-temperature", "1.0.0")
h_temperature_node.advertise("degrees")
h_humidity_node.advertise("humidity")
Homie.setup()

while True:
    time.sleep(5)
    try:
        temperature_c = dht_device.temperature
        humidity = dht_device.humidity
        print("Temp={0:0.1f}ºC  Humidity={1:0.1f}%".format(temperature_c, humidity))
        h_temperature_node.setProperty("degrees").send(temperature_c)
        h_humidity_node.setProperty("humidity").send(humidity)
    except RuntimeError as error:
        print(error.args[0])
    except Exception as error:
        dht_device.exit()
        print("Failed to retrieve data from humidity sensor")
        raise error

