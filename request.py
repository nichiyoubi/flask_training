# encoding:utf-8

import urllib
import urllib2

models = {
        'id' : 3,
        'title' : '非日用品を買ってくる',
        'description' : '車、家、クルーザー、宝石',
        'done' : False
}

url = 'http://localhost:5000/api/'

data = urllib.urlencode(models).encode("utf-8")
req = urllib2.Request(url, data)
req.add_header('Content-Type', 'application/json')
response = urllib2.urlopen(req)
print(response.read())

req = urllib2.Request(url)
response = urllib2.urlopen(req)
print(response.read())
