# _*_ coding: utf-8 _*_

from flask import Flask, make_response, render_template, request, redirect, url_for, jsonify
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import StringIO
import json

filename = 'light.json'
models = [
    {
        'id' : 1,
        'title' : '日用品を買ってくる',
        'description' : 'ミルク、チーズ、ピザ、フルーツ',
        'done' : False
    },
    {
        'id' : 2,
        'title' : 'Pythonの勉強',
        'description' : 'PythonでRESTful APIを作る',
        'done' : False
    }
]
light_value = [
	{ 'time' : 1,
	  'value' : 0
	}
]

try:
	light_file = open(filename, 'r+')
	light_json = json.load(light_file)
except:
	light_json = json.dumps(light_value)

app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello World!'

@app.route('/graph1')
def graph1():
    fig = plt.figure()
    x = range(0, 6)
    y = [0.2, 3.0, -1.2, -0,5, 1.4, 2.3]
    plt.plot(y, label="matplotlib test")
    strio = StringIO.StringIO()
    fig.savefig(strio, format="svg")
    plt.close(fig)

    strio.seek(0)
    svgstr = strio.buf[strio.buf.find("<svg"):]
    return render_template("graph.html", svgstr=svgstr.decode("utf-8"))

@app.route('/api/', methods=['GET'])
def get_api():
    print "GET!"
    return jsonify({'models': models})

@app.route('/api/', methods=['POST'])
def post_api():
    print "POST!"
    if request.headers['Content-Type'] != 'application/json':
	print(request.data)
	return jsonify(res='error') 

    print request.json
    light_value.append(request.json)
    print light_value
#    print json.dumps(light_value)
#    json.dump(light_value, light_file)
#    light_file.write(light_value)
    return jsonify(res='ok')

if __name__ == '__main__':
    app.run()
    
