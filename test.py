# -*- coding: utf-8 -*-

import RPi.GPIO as GPIO
import time
import threading
import httplib, urllib
import json

flag = True
GPIO_SW = 22
#GPIO_LED = 23

def flagon():
	global flag
	flag = True
	print "flagon"

#コールバック関数の定義
def callback(pin):
	global flag
	print flag
	if flag:
		t = threading.Timer(5, flagon)
                t.start()
                flag = False

		params = '''[{"dt":null,"pw":null,"dat": ["111","222","333"]}]'''
		headers = {"Content-type": "application/JSON","charset": "UTF-8"}
		conn = httplib.HTTPConnection("8k3kx36e19v68g.home-ip.aterm.jp")
		conn.request("POST", "/Cats/api/dataadd/marimo02/test", params, headers)
		response = conn.getresponse()
		print response.status, response.reason
		data = response.read()
		conn.close()
		print data
	else:
		print "else"

#GPIOの設定
GPIO.setmode(GPIO.BCM)
GPIO.setup(GPIO_SW, GPIO.IN, pull_up_down=GPIO.PUD_UP)
#GPIO.setup(GPIO_LED, GPIO.OUT)
#GPIO.output(GPIO_LED, GPIO.LOW)

#入力変化割り込みイベントの設定
GPIO.add_event_detect(GPIO_SW, GPIO.FALLING)
GPIO.add_event_callback(GPIO_SW, callback)

#イベント発生待ち
try:
	while True:
		time.sleep(1)
except KeyboardInterrupt:
	GPIO.cleanup()
	print("end\n")


