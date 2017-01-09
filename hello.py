# _*_ coding: utf-8 _*_

from flask import Flask, make_response, render_template, request, redirect, url_for
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import cStringIO

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello World!'

@app.route('/graph1')
def graph1():
    return 'Graph1'

if __name__ == '__main__':
    app.run()
    
