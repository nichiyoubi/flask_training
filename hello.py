# _*_ coding: utf-8 _*_

from flask import Flask, make_response, render_template, request, redirect, url_for
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg
import cStringIO

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello World!'

@app.route('/graph1')
def graph1():
    fig, ax = plt.subplots()
    ax.set_title(u'FLASK HEROKU TEST')
    x_ax = range(0, 6)
    y_ax = [0.2, 3.0, -1.2, -0.5, 1.4, 2.3]
    ax.plot(x_ax, y_ax)

    canvas = FigureCanvasAgg(fig)
    buf = cStringIO.StringIO()
    canvas.print_png(buf)
    data = buf.getvalue()

    response = make_response(data)
    response.headers['Content-Type'] = 'image/png'
    response.headers['Content-Length'] = len(data)
    return response

if __name__ == '__main__':
    app.run()
    
