# _*_ coding: utf-8 _*_

import os
from flask import Flask, make_response, render_template, request, redirect
from flask import url_for, jsonify, session
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import StringIO
import json
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']
#app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://postgres:Masanori1972@localhost/'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
# 秘密鍵は後ほどランダム化する
app.config['SECRET_KEY'] = 'The secret key which ciphers the cookie'
db = SQLAlchemy(app)

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(64))
    email = db.Column(db.String(64), unique=True)

    def __init__(self, name, email):
        self.name = name
        self.email = email
        
    def __repr__(self):
        return '<User %r>' % self.name

class LightValue(db.Model):
    __tablename__ = 'light_value'
    id = db.Column(db.Integer, primary_key = True)
    mac = db.Column(db.String(8))
    time = db.Column(db.Integer)
    light = db.Column(db.Float)
    
    def __init__(self, mac, time, light):
        self.mac = mac
        self.time = time
        self.light = light
    
    def __repr__(self):
        return '<Mac %r Time %d, Light %f>' % (self.mac, self.time, self.light)

# 表紙ページ（ログイン画面）
@app.route('/', methods=['GET'])
def index():
    return render_template("index.html")

# エラーハンドラ
@app.errorhandler(404)
@app.errorhandler(405)
def error_handler(error):
    return redirect(url_for('index'))

# ログイン処理
@app.route('/login', methods=['POST'])
def login():
    if _is_account_valid():
        session['email'] = request.form['email']
        return redirect(url_for('device'))
    return redirect(url_for('index'))

# アカウントのチェック
def _is_account_valid():
    if request.form.get('email') is None:
        return False
    else:
        return True

# ログアウト処理
@app.route('/logout')
def logout():
    # セッションからユーザー名を取り除く
    session.pop('email', None)
    # 表紙（ログインページ）にリダイレクトする
    return redirect(url_for('index'))

# デバイス一覧
@app.route('/device')
def device():
    # セッションにemailが保存されていなければ表紙ページにリダイレクトする
    if session.get('email') is not None:
        devices = db.engine.execute("select distinct mac from Light_Value;")
        return render_template("device.html", lights = devices)
    else:
        return redirect(url_for('index'))

# グラフ表示
@app.route('/graph1')
def graph1():
    # セッションにemailが保存されていなければ表紙ページにリダイレクトする
    if session.get('email') is not None:
        fig = plt.figure()
        lights = LightValue.query.filter().all()
        nx = np.array([])
        ny = np.array([])
        for x in lights:
	    nx = np.append(nx, x.time)
	    ny = np.append(ny, x.light)
        plt.plot(nx, ny, label="matplotlib test")
        strio = StringIO.StringIO()
        fig.savefig(strio, format="svg")
        plt.close(fig)

        strio.seek(0)
        svgstr = strio.buf[strio.buf.find("<svg"):]
        return render_template("graph.html",
                           svgstr=svgstr.decode("utf-8"), title="sensor value")
    else:
        return redirect(url_for('index'))

@app.route('/api/', methods=['GET'])
def get_api():
    # セッションにemailが保存されていなければ表紙ページにリダイレクトする
    if session.get('email') is not None:
        print "GET!"
        lights = LightValue.query.filter().all()
        if (len(lights) > 0):
	    result = []
	    for x in lights:
	        light = { 'mac' : x.mac, 'time' : x.time, 'value' : x.light }
	        result.append(light)
	    return jsonify({'light' : result})
        else:
	    return jsonify(res='error')
    else:
        return redirect(url_for('index'))

@app.route('/api/<int:id>', methods=['GET'])
def get_api_id(id):
    # セッションにemailが保存されていなければ表紙ページにリダイレクトする
    if session.get('email') is not None:
        lights = LightValue.query.filter(LightValue.time == id).all()
        if (len(lights) > 0):
	    light = { 'mac' : lights[0].mac, 'time' : lights[0].time, 'value' : lights[0].light }
	    return jsonify({'light' : light})
        else:
	    return jsonify(res='error')
    else:
        return redirect(url_for('index'))

@app.route('/api/', methods=['POST'])
def post_api():
    # セッションにemailが保存されていなければ表紙ページにリダイレクトする
    if session.get('email') is not None:
        if request.headers['Content-Type'] != 'application/json':
	    return jsonify(res='error') 

        light = LightValue(request.json['mac'], request.json['time'], request.json['value'])
        db.session.add(light)
        db.session.commit()
        return jsonify(res='ok')
    else:
        return redirect(url_for('index'))

@app.route('/api/', methods=['DELETE'])
def delete_api():
    # セッションにemailが保存されていなければ表紙ページにリダイレクトする
    if session.get('email') is not None:
        lights = LightValue.query.filter().all()
        if (len(lights) > 0):
            for x in lights:
                db.session.delete(x)
                db.session.commit()
	    return jsonify(res='ok') 
        else:
	    return jsonify(res='error')
    else:
        return redirect(url_for('index'))

@app.route('/api/<int:id>', methods=['DELETE'])
def delete_api_id(id):
    # セッションにemailが保存されていなければ表紙ページにリダイレクトする
    if session.get('email') is not None:
        lights = LightValue.query.filter(LightValue.id == id).first()
        db.session.delete(lights)
        db.session.commit()
        return jsonify(res='ok')
    else:
        return redirect(url_for('index'))

if __name__ == '__main__':
    app.run()
    
