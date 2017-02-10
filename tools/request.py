# encoding:utf-8

import sys
import argparse
import urllib
import urllib2
import cookielib
import json
import random

parser = argparse.ArgumentParser()
parser.add_argument("-a", "--add", action="store_true", 
		help="add sensor data.")
parser.add_argument("-d", "--delete", action="store_true", 
		help="delete sensor data.")
args = parser.parse_args()

url_login = 'http://localhost:5000/api/login'
# url_login = 'https://quiet-earth-43690.herokuapp.com/login'
url_light = 'http://localhost:5000/api/light'
# url_light = 'https://quiet-earth-43690.herokuapp.com/light'

opener = urllib2.build_opener()

def login():
	req = urllib2.Request(url_login,
			'username=%s&password=%s' % ('admin', 'administrator'))
	opener.add_handler(urllib2.HTTPCookieProcessor(cookielib.CookieJar()))
	conn = opener.open(req)
	print "login"
	print(conn.read())

def add():
	light = { 'mac' : 'abcdef01', 'time' : 1, 'value' : 400 }
	for mac in range(1, 4):
	    light['mac'] = 'abcdef' + str(mac)
	    for time in range(11,21):
		light['time'] = time
		light['value'] = random.uniform(1, 500)
		req = urllib2.Request(url_light, json.dumps(light))
		req.add_header('Content-Type', 'application/json')
		conn = opener.open(req)
		print(conn.read())

def get():
	req = urllib2.Request(url_light)
	conn = opener.open(req)
	print(conn.read())

def delete():
	req = urllib2.Request(url_light)
	req.get_method = lambda: 'DELETE'
	conn = opener.open(req)
	print(conn.read())

if (__name__ == '__main__'):
	login()
	
	if args.add:
		print "add sensor data."
		add()
	if args.delete:
		print "delete sensor data."
		delete()
	get()


