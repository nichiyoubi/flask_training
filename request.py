# encoding:utf-8

import urllib
import urllib2
import json

models = {
        'id' : 3,
        'title' : '非日用品を買ってくる',
        'description' : '車、家、クルーザー、宝石',
        'done' : False
    }
light = { 'time' : 1, 'value' : 400 }

url = 'http://localhost:5000/api/'

req = urllib2.Request(url, json.dumps(light))
req.add_header('Content-Type', 'application/json')
response = urllib2.urlopen(req)
print(response.read())

req = urllib2.Request(url)
response = urllib2.urlopen(req)
print(response.read())
