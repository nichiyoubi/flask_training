# _*_ coding: utf-8 _*_

from robotapp import app
from robotapp import db
from robotapp import model_users as user
from robotapp import model_light_sensor as sensor 
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
    if user.is_account_valid():
        session['username'] = request.form['username']
	if request.form['username'] == 'admin':
            return redirect(url_for('users'))
        else:
            return redirect(url_for('device'))
    return redirect(url_for('index'))

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
	users = user.User.query.filter().all()
        return render_template("users.html", users = users)
    else:
        return redirect(url_for('index'))

# グラフ表示
@app.route('/graph/<mac>')
def graph(mac):
    # セッションにusernameが保存されていなければ表紙ページにリダイレクトする
    if session.get('username') is not None:
        fig = plt.figure()
        lights = sensor.LightValue.query.filter(sensor.LightValue.mac == mac).all()
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
        lights = sensor.LightValue.query.filter(sensor.LightValue.mac == mac).all()
        return render_template("light_table.html", lights = lights)
    else:
        return redirect(url_for('index'))

# ユーザー管理画面の表示
@app.route('/admin/users', methods = ['GET'])
def admin_user():
    # セッションにusernameが保存されていなければ表紙ページにリダイレクトする
    if session.get('username') is not None:
        if session.get('username') == 'admin':
	    users = user.User.query.filter().all()
	    return render_template("admin_users.html", users = users)
	else:
	    return redirect(url_for('device'))
    else:
        return redirect(url_for('index'))

# ユーザー管理画面の表示
@app.route('/admin/users', methods = ['POST'])
def admin_add_user():
    # セッションにusernameが保存されていなければ表紙ページにリダイレクトする
    print session.get('username')
    if session.get('username') is not None:
	print "session ok"
        if session.get('username') == 'admin':
	    print "session is admin's"
            db.session.add(user.User(request.form['newusername'],
		                     request.form['newpassword']))
            db.session.commit()
	    users = user.User.query.filter().all()
	    return render_template("admin_users.html", users = users)
	else:
	    print "session is not admin's"
	    return redirect(url_for('device'))
    else:
	print "session error"
        return redirect(url_for('index'))
