# encoding:utf-8

import urllib
import urllib2
import cookielib
import json
import random

url_login = 'http://localhost:5000/api/login'
# url_login = 'https://quiet-earth-43690.herokuapp.com/login'
url_light = 'http://localhost:5000/api/light'
# url_light = 'https://quiet-earth-43690.herokuapp.com/light'


req = urllib2.Request(url_login, 'username=%s&password=%s' % ('admin', 'administrator'))
opener = urllib2.build_opener()
opener.add_handler(urllib2.HTTPCookieProcessor(cookielib.CookieJar()))
conn = opener.open(req)
print "login"
print(conn.read())

light = { 'mac' : 'abcdef01', 'time' : 1, 'value' : 400 }
for mac in range(1, 4):
    # print mac
    light['mac'] = 'abcdef' + str(mac)
    for time in range(11,21):
        # print time
	light['time'] = time
	light['value'] = random.uniform(1, 500)
	req = urllib2.Request(url_light, json.dumps(light))
	req.add_header('Content-Type', 'application/json')
	conn = opener.open(req)
	print(conn.read())

req = urllib2.Request(url_light)
conn = opener.open(req)
print(conn.read())

