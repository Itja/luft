#!/usr/bin/env python3
import time
import board
import adafruit_dht

from homie.device_temperature_humidity import Device_Temperature_Humidity

dht_device = adafruit_dht.DHT22(board.D4)

sleep_seconds = 5

temp_hum = Device_Temperature_Humidity(device_id="air01", name="Test Temp Hum", mqtt_settings={"MQTT_BROKER": "10.10.10.8"}, temp_units="ºC")

while True:
    time.sleep(sleep_seconds)

    try:
        temperature_c = dht_device.temperature
        humidity = dht_device.humidity
        print("Temp={0:0.1f}ºC  Humidity={1:0.1f}%".format(temperature_c, humidity))
        temp_hum.update_temperature(temperature_c)
        temp_hum.update_humidity(humidity)
    except RuntimeError as error:
        print(error.args[0])
    except Exception as error:
        dht_device.exit()
        raise error
