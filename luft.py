#!/usr/bin/env python3
import time
import board
import adafruit_dht

dht_device = adafruit_dht.DHT22(board.D4)

while True:
    time.sleep(2)
    try:
        temperature_c = dht_device.temperature
        humidity = dht_device.humidity
        print("Temp={0:0.1f}ºC  Humidity={1:0.1f}%".format(temperature_c, humidity))
    except RuntimeError as error:
        print(error.args[0])
    except Exception as error:
        dht_device.exit()
        print("Failed to retrieve data from humidity sensor")
        raise error

