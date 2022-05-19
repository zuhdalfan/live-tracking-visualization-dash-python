import json
from time import sleep
from flask import request
import serial
import datetime
import csv
import requests

ser = serial.Serial('/dev/serial/by-id/usb-STMicroelectronics_STM32_Virtual_ComPort_3353336A3539-if00', 2000000, timeout=0)
ser.flushInput()

while 1:
	sleep(0.1)
	data = ser.readline().decode('utf-8', 'ignore')
#	data = str(data)
	# print(len(data))
	if len(data)>1:
		sendData = {
			'x': data.split(',')[1],
			'y': data.split(',')[2],
			'z': data.split(',')[3]
			}
		print(sendData)
		try:
			response = requests.post('http://localhost:8033/data',json={'POS':sendData})
			print(f">>> response.content {response.content}")
			print(f">>> response.status {response.status_code}")
			ser.flushInput()
		except Exception as e:
			print(f">>> request error {e.args}")

