# _*_ coding: utf-8 _*_

from flask import Flask, make_response, render_template, request, redirect, url_for
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import StringIO

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello World!'

@app.route('/graph1')
def graph1():
#    return 'Graph1'
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

if __name__ == '__main__':
    app.run()
    
