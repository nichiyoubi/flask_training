# _*_ coding: utf-8 _*_

from robotapp import app
from robotapp import db
from flask import request, redirect
from flask_sqlalchemy import SQLAlchemy

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

# アカウントのチェック
def is_account_valid():
    if request.form.get('username') is None:
        return False
    else:
	users = User.query.filter().all()
	for user in users:
	    if (request.form['username'] == user.username) and (request.form['password'] == user.password):
	         return True
        return False


