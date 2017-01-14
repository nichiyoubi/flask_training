# encoding:utf-8

import urllib
import urllib2
import json


url = 'http://localhost:5000/api/'
# url = 'https://quiet-earth-43690.herokuapp.com/api/'

req = urllib2.Request(url)
req.get_method = lambda: 'DELETE'
response = urllib2.urlopen(req)
print(response.read())
