# _*_ coding: utf-8 _*_
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']
# app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://postgres:Masanori1972@localhost/'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
# 秘密鍵は後ほどランダム化する
app.config['SECRET_KEY'] = 'The secret key which ciphers the cookie'

db = SQLAlchemy(app)

import robotapp.model_users
import robotapp.model_light_sensor
import robotapp.views
import robotapp.apis
