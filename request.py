# encoding:utf-8

import urllib
import urllib2
import json
import random

light = { 'time' : 1, 'value' : 400 }

# url = 'http://localhost:5000/api/'
url = 'https://quiet-earth-43690.herokuapp.com/api/'

light['time'] = random.randint(1, 10)
light['value'] = random.uniform(1, 500)
req = urllib2.Request(url, json.dumps(light))
req.add_header('Content-Type', 'application/json')
response = urllib2.urlopen(req)
print(response.read())

req = urllib2.Request(url)
response = urllib2.urlopen(req)
print(response.read())
