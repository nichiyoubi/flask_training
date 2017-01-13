# _*_ coding: utf-8 _*_

from flask import Flask, make_response, render_template, request, redirect, url_for, jsonify
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import StringIO
import json

app = Flask(__name__)

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
    return jsonify({'models': models})

@app.route('/api/', methods=['POST'])
def post_api():
    print "POST!"
    if request.headers['Content-Type'] != 'application/json':
	print(request.data)
	return jsonify(res='error') 

    print request.headers['Content-Type']
    print request.data
#    print json.loads(request.data)
    return jsonify(res='ok')

if __name__ == '__main__':
    app.run()
    
