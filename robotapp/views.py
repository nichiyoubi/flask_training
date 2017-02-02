# _*_ coding: utf-8 _*_

from robotapp import app
from flask import make_response, render_template, request, redirect
from flask import url_for, jsonify, session
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import StringIO
import json
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy(app)

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(64))
    password = db.Column(db.String(128), unique=True)

    def __init__(self, username, password):
        self.username = username
        self.password = password 
        
    def __repr__(self):
        return '<User %r>' % self.username

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
        session['username'] = request.form['username']
	if request.form['username'] == 'admin':
            return redirect(url_for('users'))
        else:
            return redirect(url_for('device'))
    return redirect(url_for('index'))

# アカウントのチェック
def _is_account_valid():
    if request.form.get('username') is None:
        return False
    else:
	users = User.query.filter().all()
	for user in users:
	    if (request.form['username'] == user.username) and (request.form['password'] == user.password):
	         return True
        return False

# ログアウト処理
@app.route('/logout')
def logout():
    # セッションからユーザー名を取り除く
    session.pop('username', None)
    # 表紙（ログインページ）にリダイレクトする
    return redirect(url_for('index'))

# デバイス一覧
@app.route('/device')
def device():
    # セッションにusernameが保存されていなければ表紙ページにリダイレクトする
    if session.get('username') is not None:
        devices = db.engine.execute("select distinct mac from Light_Value;")
        return render_template("device.html", lights = devices)
    else:
        return redirect(url_for('index'))

# ユーザー一覧
@app.route('/users')
def users():
    # セッションにusernameが保存されていなければ表紙ページにリダイレクトする
    if session.get('username') is not None:
	users = User.query.filter().all()
        return render_template("users.html", users = users)
    else:
        return redirect(url_for('index'))

# グラフ表示
@app.route('/graph/<mac>')
def graph(mac):
    # セッションにusernameが保存されていなければ表紙ページにリダイレクトする
    if session.get('username') is not None:
        fig = plt.figure()
        lights = LightValue.query.filter(LightValue.mac == mac).all()
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

# 表の表示
@app.route('/table/<mac>')
def table(mac):
    # セッションにusernameが保存されていなければ表紙ページにリダイレクトする
    if session.get('username') is not None:
        lights = LightValue.query.filter(LightValue.mac == mac).all()
        return render_template("light_table.html", lights = lights)
    else:
        return redirect(url_for('index'))

#############################################################################
# API
#############################################################################

# ログイン処理
@app.route('/api/login', methods=['POST'])
def api_login():
    if _is_account_valid():
        session['username'] = request.form['username']
	return jsonify(res='ok')
    return jsonify(res='error')

# ログアウト処理
@app.route('/api/logout')
def api_logout():
    # セッションからユーザー名を取り除く
    session.pop('username', None)
    return jsonify(res='ok')


# LightValueテーブルの一覧の取得
@app.route('/api/light', methods=['GET'])
def api_get_lights():
    # セッションにusernameが保存されていなければ表紙ページにリダイレクトする
    if session.get('username') is not None:
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
	return jsonify(res='no session')

# LightValueテーブルのレコードの取得
@app.route('/api/light/<int:id>', methods=['GET'])
def api_get_light(id):
    # セッションにusernameが保存されていなければ表紙ページにリダイレクトする
    if session.get('username') is not None:
        lights = LightValue.query.filter(LightValue.time == id).all()
        if (len(lights) > 0):
	    light = { 'mac' : lights[0].mac, 'time' : lights[0].time, 'value' : lights[0].light }
	    return jsonify({'light' : light})
        else:
	    return jsonify(res='error')
    else:
	return jsonify(res='no session')

# LightValueテーブルへのレコードの追加
@app.route('/api/light', methods=['POST'])
def api_post_light():
    # セッションにusernameが保存されていなければ表紙ページにリダイレクトする
    if session.get('username') is not None:
        if request.headers['Content-Type'] != 'application/json':
	    return jsonify(res='error') 

        light = LightValue(request.json['mac'], request.json['time'], request.json['value'])
        db.session.add(light)
        db.session.commit()
        return jsonify(res='ok')
    else:
	return jsonify(res='no session')

# LightValueテーブルへの全レコード削除
@app.route('/api/light', methods=['DELETE'])
def api_delete_lights():
    # セッションにusernameが保存されていなければ表紙ページにリダイレクトする
    if session.get('username') is not None:
        lights = LightValue.query.filter().all()
        if (len(lights) > 0):
            for x in lights:
                db.session.delete(x)
                db.session.commit()
	    return jsonify(res='ok') 
        else:
	    return jsonify(res='error')
    else:
	return jsonify(res='error')

# LightValueテーブルへのレコードの削除
@app.route('/api/light/<int:id>', methods=['DELETE'])
def api_delete_light(id):
    # セッションにusernameが保存されていなければ表紙ページにリダイレクトする
    if session.get('username') is not None:
        lights = LightValue.query.filter(LightValue.id == id).first()
        db.session.delete(lights)
        db.session.commit()
        return jsonify(res='ok')
    else:
	return jsonify(res='error')

