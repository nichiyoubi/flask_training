# _*_ coding: utf-8 _*_

from robotapp import app
from robotapp import db
from robotapp import models
from flask import request, redirect, url_for, jsonify, session
import json
from flask_sqlalchemy import SQLAlchemy


#############################################################################
# API
#############################################################################

# ログイン処理
@app.route('/api/login', methods=['POST'])
def api_login():
    if models.is_account_valid():
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
        lights = models.LightValue.query.filter().all()
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
        lights = models.LightValue.query.filter(LightValue.time == id).all()
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

        light = models.LightValue(request.json['mac'], request.json['time'], request.json['value'])
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
        lights = models.LightValue.query.filter().all()
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
        lights = models.LightValue.query.filter(LightValue.id == id).first()
        db.session.delete(lights)
        db.session.commit()
        return jsonify(res='ok')
    else:
	return jsonify(res='error')

