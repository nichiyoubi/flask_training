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


