# _*_ coding: utf-8 _*_

from flask import Flask, make_response, render_template, request, redirect, url_for, jsonify
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import StringIO
import json
import sqlalchemy
from flask_sqlalchemy import SQLAlchemy


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
light_value = []
light_sensor_time = []
light_sensor_value = []

try:
	light_file = open(filename, 'r+')
        light_file.seek(0)
        light_value = json.load(light_file)
except:
        light_file = open(filename, 'w')


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://localhost/mydb'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(app)


@app.route('/')
def hello_world():
    return 'Hello World!'

@app.route('/graph1')
def graph1():
    global light_sensor_time
    global light_sensor_value
    fig = plt.figure()
    nx = np.array(light_sensor_time)
    ny = np.array(light_sensor_value)
    plt.plot(nx, ny, label="matplotlib test")
    strio = StringIO.StringIO()
    fig.savefig(strio, format="svg")
    plt.close(fig)

    strio.seek(0)
    svgstr = strio.buf[strio.buf.find("<svg"):]
    return render_template("graph.html",
                           svgstr=svgstr.decode("utf-8"), title="sensor value")

@app.route('/api/', methods=['GET'])
def get_api():
    global light_value
    print "GET!"
    return jsonify({'light' : light_value})

@app.route('/api/', methods=['POST'])
def post_api():
    global light_value
    global light_sensor_time
    global light_sensor_value
    print "POST!"
    if request.headers['Content-Type'] != 'application/json':
	return jsonify(res='error') 

    light_value.append(request.json)
    light_sensor_time.append(request.json['time'])
    light_sensor_value.append(request.json['value'])
    return jsonify(res='ok')

@app.route('/api/', methods=['DELETE'])
def delete_api():
    global light_value
    print "DELETE!"
    light_value = []
    light_file.seek(0)
    json.dump(light_value, light_file)
    return jsonify(res='ok')


if __name__ == '__main__':
    app.run()
    light_file.seek(0)
    json.dump(light_value, light_file)
    
